import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
TEST_TMP=(ROOT/'work/tests').resolve()
assert TEST_TMP.is_relative_to(ROOT.resolve())
TEST_TMP.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'scripts'))
import femo
import install_skill

class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=TEST_TMP);self.root=Path(self.temp.name)/'projeto';femo.init_project(self.root)
    def tearDown(self):self.temp.cleanup()
    def test_init_preserves_brief(self):
        (self.root/'briefing.md').write_text('aprovado',encoding='utf-8');femo.init_project(self.root)
        self.assertEqual((self.root/'briefing.md').read_text(encoding='utf-8'),'aprovado')
    def test_escape_rejected(self):
        with self.assertRaises(femo.ProjectError):femo.contained(self.root,'../privado.mp4')
    def test_caption_timeline_and_order(self):
        segments=[{'source':'a.mp4','start':20.,'end':25.,'offset':5.}]
        mapped=femo.remap_words(segments,[{'source':'a.mp4','start':21.,'end':21.5,'text':'marca'}])
        self.assertEqual(mapped[0]['start'],6.)
        self.assertIn('00:00:06,000 --> 00:00:06,500',femo.words_to_srt(mapped))
        self.assertNotIn(chr(92)+'n',femo.words_to_srt(mapped))
    def test_cut_inside_word_rejected(self):
        with self.assertRaises(femo.ProjectError):
            femo.remap_words([{'source':'a','start':1.,'end':2.,'offset':0.}],
                             [{'source':'a','start':.8,'end':1.3,'text':'palavra'}])
    def test_install_portable_and_idempotent(self):
        result=install_skill.install(self.root,'both')
        self.assertEqual(len(result),2)
        for scope in ['.agents','.claude']:
            base=self.root/scope/'skills/femo-ai-studio'
            self.assertTrue((base/'scripts/femo.py').is_file())
            self.assertTrue((base/'references/video.md').is_file())
            self.assertTrue((base/'examples/carrossel-sobrancelhas.md').is_file())
        self.assertIn('já instalado',install_skill.install(self.root,'claude')[0]['status'])
    def test_install_does_not_overwrite(self):
        dest=self.root/'.claude/skills/femo-ai-studio';dest.mkdir(parents=True)
        (dest/'SKILL.md').write_text('meu trabalho',encoding='utf-8')
        with self.assertRaises(ValueError):install_skill.install(self.root,'both')
        self.assertEqual((dest/'SKILL.md').read_text(encoding='utf-8'),'meu trabalho')
        self.assertFalse((self.root/'.agents/skills/femo-ai-studio').exists())

@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg e FFprobe necessários para mídia sintética')
class MediaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(dir=TEST_TMP);cls.root=Path(cls.temp.name)/'projeto teste';femo.init_project(cls.root)
        cls.one=cls.root/'01_brutos/tomada com espaço.mp4';cls.two=cls.root/"01_brutos/tomada d'apoio.mp4"
        femo.run([femo.executable('ffmpeg'),'-hide_banner','-loglevel','error','-nostdin','-n','-f','lavfi','-i','testsrc2=size=320x180:rate=24','-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','2.4','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',cls.one])
        femo.run([femo.executable('ffmpeg'),'-hide_banner','-loglevel','error','-nostdin','-n','-f','lavfi','-i','testsrc2=size=128x192:rate=25','-t','2','-c:v','libx264','-pix_fmt','yuv420p',cls.two])
        cls.hashes=[cls.one.read_bytes(),cls.two.read_bytes()]
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def edl(self,**updates):
        value={'schema_version':1,'project_root':'..','output':{'width':96,'height':160,'fps':24,'fit':'contain'},'segments':[
            {'source':self.one.relative_to(self.root).as_posix(),'start':.2,'end':1.2},
            {'source':self.two.relative_to(self.root).as_posix(),'start':.1,'end':1.1}]}
        value.update(updates);path=self.root/'05_projeto/edl.json';femo.write_json(path,value);return path
    def test_inventory_audio_and_geometry(self):
        result=femo.inventory(self.root,True)
        self.assertEqual(len(result['sources']),2)
        self.assertEqual(sorted(x['has_audio'] for x in result['sources']),[False,True])
        self.assertTrue(all(len(x['sha256'])==64 for x in result['sources']))
    def test_bounds_and_nan_rejected(self):
        for end in [20.,float('nan')]:
            with self.assertRaises(femo.ProjectError):
                femo.validate(self.edl(segments=[{'source':self.one.relative_to(self.root).as_posix(),'start':0,'end':end}]))
    def test_odd_dimensions_rejected(self):
        with self.assertRaises(femo.ProjectError):femo.validate(self.edl(output={'width':95,'height':160,'fps':24}))
    def test_hdr_rejected(self):
        real=femo.source_info(self.one);real['video']['color_transfer']='arib-std-b67'
        with patch.object(femo,'source_info',return_value=real):
            with self.assertRaises(femo.ProjectError):femo.validate(self.edl())
    def test_render_mixed_geometry_audio_and_versions(self):
        path=self.edl();a=femo.render(path,True);b=femo.render(path,False)
        self.assertTrue(a['technical_checks_passed']);self.assertTrue(b['technical_checks_passed'])
        self.assertNotEqual(a['output'],b['output']);self.assertTrue(a['creative_review_pending'])
        self.assertLess(abs(a['actual_seconds']-2.),.15)
        self.assertEqual([self.one.read_bytes(),self.two.read_bytes()],self.hashes)
        # Decode the complete output: metadata alone would not prove a readable file.
        femo.run([femo.executable('ffmpeg'),'-v','error','-i',a['output'],'-f','null','-'])
    def test_non_frame_aligned_durations_and_caption_offsets(self):
        path=self.edl(segments=[
            {'source':self.one.relative_to(self.root).as_posix(),'start':.2,'end':1.23},
            {'source':self.two.relative_to(self.root).as_posix(),'start':.1,'end':1.11}])
        data,root,segments,caption,expected=femo.load_edl(path)
        self.assertAlmostEqual(segments[1]['offset'],25/24)
        mapped=femo.remap_words(segments,[{'source':self.two.relative_to(self.root).as_posix(),'start':.2,'end':.4,'text':'marca'}])
        self.assertAlmostEqual(mapped[0]['start'],25/24+.1)
        result=femo.render(path,True)
        self.assertTrue(result['technical_checks_passed'])
        self.assertAlmostEqual(result['actual_seconds'],50/24,delta=.05)

    def test_caption_file_and_burn(self):
        path=self.edl();words=self.root/'05_projeto/palavras.json'
        femo.write_json(words,{'words':[{'source':self.one.relative_to(self.root).as_posix(),'start':.3,'end':.6,'text':'FEMO'}]})
        out=femo.captions(path,words)
        data=json.loads(path.read_text(encoding='utf-8'));data['caption_srt']=out['caption_srt_for_edl'];data['caption_font']='Arial';femo.write_json(path,data)
        result=femo.render(path,True)
        self.assertTrue(result['technical_checks_passed']);self.assertTrue(result['caption_font_visual_check_pending'])

if __name__=='__main__':unittest.main()
