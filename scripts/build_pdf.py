"""Gera o guia editorial FEMO com navegação e botões clicáveis."""
from pathlib import Path
import json
import math
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from fontTools.ttLib import TTFont as FTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT=Path(__file__).resolve().parents[1]
W,H=700,990
M=52
CONTENT=W-2*M
TOTAL=16
GREEN='#071E18'; SUPPORT='#123A2C'; GREY='#E5E5E5'; ORANGE='#E35C0A'; WHITE='#FFFFFF'
REPO='https://github.com/agenciafemo/femo-ai-studio'
ZIP=REPO+'/archive/refs/heads/main.zip'
URL={
 'repo':REPO,'zip':ZIP,'install':REPO+'/blob/main/docs/INSTALACAO.md',
 'prompts':REPO+'/blob/main/docs/PROMPTS.md','research':REPO+'/blob/main/docs/PESQUISA.md',
 'video':REPO+'/blob/main/references/video.md','design':REPO+'/blob/main/references/design.md',
 'example':REPO+'/blob/main/examples/carrossel-sobrancelhas.md',
 'claude':'https://code.claude.com/docs/en/setup','codex':'https://developers.openai.com/codex/app/',
 'ffmpeg':'https://ffmpeg.org/download.html','python':'https://www.python.org/downloads/',
 'hyperframes':'https://github.com/heygen-com/hyperframes','videouse':'https://github.com/browser-use/video-use',
 'canva':'https://www.canva.com/','kairo':'https://app.kairogen.ai/',
 'anatomy':'https://anatomiadoprompt.vercel.app/','whisper':'https://github.com/SYSTRAN/faster-whisper'
}
WORK=ROOT/'work/pdf';WORK.mkdir(parents=True,exist_ok=True)
for name,weight in [('Inter',400),('InterLight',300),('InterBold',600)]:
 out=WORK/(name+'.ttf')
 if not out.exists():
  font=FTFont(ROOT/'assets/fonts/InterVariable.ttf')
  static=instantiateVariableFont(font,{'wght':weight,'opsz':14},inplace=False)
  static.save(out)
 pdfmetrics.registerFont(TTFont(name,str(out)))
pdfmetrics.registerFontFamily('Inter',normal='Inter',bold='InterBold',italic='Inter',boldItalic='InterBold')
OUT=ROOT/'docs/GUIA-FEMO-AI-STUDIO.pdf';OUT.parent.mkdir(exist_ok=True)
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
c.setTitle('FEMO AI Studio | Guia de vídeo e design com Claude e Codex')
c.setAuthor('Agência FEMO');c.setSubject('Guia prático com links clicáveis e workflow local')
LOGO=ImageReader(str(ROOT/'assets/brand/femo-logo.png'))
page=0;light=False;INK=WHITE;MUTED='#B4C7BF';boxes=[]

def para(text,x,y,w=CONTENT,size=14,leading=None,color=None,font='Inter'):
 style=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.48,textColor=HexColor(color or INK),spaceAfter=0)
 p=Paragraph(text,style);_,height=p.wrap(w,2000)
 if y-height<66:raise ValueError(f'Texto fora da área segura na página {page}: {text[:80]} -> {y-height}')
 p.drawOn(c,x,y-height);boxes.append({'page':page,'type':'text','rect':[x,y-height,x+w,y]})
 return y-height

def line(x,y,w,color=None):
 c.setStrokeColor(HexColor(color or ('#BAC6BF' if light else '#28483B')));c.setLineWidth(.7);c.line(x,y,x+w,y)

def pill(text,x,y,w=None):
 w=w or pdfmetrics.stringWidth(text,'InterBold',10)+22
 c.setFillColor(HexColor(SUPPORT if not light else '#D3DDD6'));c.roundRect(x,y-25,w,25,12,fill=1,stroke=0)
 para(escape(text),x+11,y-6,w-20,10,12,color=('#E5E5E5' if not light else GREEN),font='InterBold')

def button(label,x,y,w,url,primary=False):
 h=42
 if y-h<66:raise ValueError('Botão fora da área segura')
 c.setFillColor(HexColor(ORANGE if primary else (SUPPORT if not light else '#D7DFDA')))
 c.roundRect(x,y-h,w,h,8,fill=1,stroke=0)
 color=GREEN if primary else (WHITE if not light else GREEN)
 size=11.5
 if pdfmetrics.stringWidth(label,'InterBold',size)>w-38:size=10.4
 c.setFillColor(HexColor(color));c.setFont('InterBold',size);c.drawString(x+15,y-26,label)
 c.setFont('Inter',13);c.drawRightString(x+w-14,y-26,'→')
 rect=(x,y-h,x+w,y)
 if url.startswith('#p'):c.linkAbsolute(label,url[1:],rect,thickness=0)
 else:c.linkURL(url,rect,relative=0,thickness=0)
 boxes.append({'page':page,'type':'button','label':label,'rect':list(rect),'url':url})
 return y-h

def panel(x,y,w,h,fill=None):
 c.setFillColor(HexColor(fill or (SUPPORT if not light else '#F4F6F3')))
 c.roundRect(x,y-h,w,h,11,fill=1,stroke=0)

def note(text,x,y,w=CONTENT):
 style=ParagraphStyle('n',fontName='Inter',fontSize=12,leading=18,textColor=HexColor(INK))
 p=Paragraph(text,style);_,h=p.wrap(w-34,1200);h+=28
 if y-h<66:raise ValueError(f'Nota longa página {page}')
 panel(x,y,w,h);c.setFillColor(HexColor(ORANGE));c.rect(x,y-h+12,3,h-24,fill=1,stroke=0)
 p.drawOn(c,x+18,y-h+14);return y-h

def base(is_light=False):
 global page,light,INK,MUTED
 page+=1;light=is_light;INK=GREEN if light else WHITE;MUTED='#476157' if light else '#B4C7BF'
 c.setFillColor(HexColor(GREY if light else GREEN));c.rect(0,0,W,H,fill=1,stroke=0)
 c.bookmarkPage('p'+str(page))
 if light:
  c.setFillColor(HexColor(GREEN));c.roundRect(M-10,H-62,132,36,6,fill=1,stroke=0)
 c.drawImage(LOGO,M,H-54,width=110,height=25.7,mask='auto')
 c.setFillColor(HexColor(MUTED));c.setFont('Inter',9);c.drawRightString(W-M,H-40,'GUIA PRÁTICO · 2026')
 for i in range(TOTAL):
  c.setFillColor(HexColor(ORANGE if i==page-1 else ('#C0CDC5' if light else '#214334')))
  c.roundRect(W-M-16*6+i*6,H-76,4,3,1,fill=1,stroke=0)
 line(M,57,CONTENT)
 c.setFont('Inter',8.5);c.setFillColor(HexColor(MUTED));c.drawString(M,37,'FEMO AI Studio · Movimento com direção')
 c.drawRightString(W-M,37,f'{page:02} / {TOTAL}')

def heading(label,title,desc=None):
 para(label.upper(),M,875,CONTENT,10.5,13,color=(GREEN if light else ORANGE),font='InterBold')
 y=para(title,M,841,CONTENT,37,42,font='InterLight')
 if desc:y=para(desc,M,y-18,CONTENT,14,21,color=MUTED)
 return y-35

def step(n,title,body,y,height=112):
 panel(M,y,CONTENT,height)
 para(f'{n:02}',M+18,y-19,38,22,25,color=ORANGE,font='InterLight')
 para(title,M+72,y-18,CONTENT-94,19,24,font='InterBold')
 para(body,M+72,y-52,CONTENT-94,12.5,18,color=MUTED)
 return y-height-14

def finish():c.showPage()

# 01
base();pill('CLAUDE + CODEX',M,865,139)
para('Da pasta de brutos<br/>à primeira edição.',M,790,CONTENT,49,55,font='InterLight')
para('Vídeo e design<br/><font color="#E35C0A">com direção.</font>',M,650,CONTENT,43,49,font='InterLight')
para('Um pacote da FEMO para organizar materiais, orientar a IA e entregar versões que você consegue revisar.',M,520,540,16,24,color=MUTED)
# Ilustração original: pastas e timeline, sem simular um software real.
panel(M,403,CONTENT,154)
for i,(name,w) in enumerate([('Brutos',135),('Referências',165),('Marca',126)]):
 x=M+20+sum([155,185,0][:i]);c.setFillColor(HexColor('#234B38'));c.roundRect(x,345,w,38,6,fill=1,stroke=0)
 para(name,x+12,370,w-24,12,15)
line(M+22,315,CONTENT-44,'#54715F')
for i,w in enumerate([92,150,70,117]):
 x=M+22+sum([102,160,80,0][:i]);c.setFillColor(HexColor(ORANGE if i==2 else '#41624F'));c.roundRect(x,280,w,21,3,fill=1,stroke=0)
button('Baixar o pacote completo',M,215,CONTENT,URL['zip'],True)
button('Abrir o repositório',M,160,CONTENT,URL['repo'])
para('Guia com botões clicáveis. A edição acontece em um ambiente com acesso aos arquivos e ferramentas.',M,99,CONTENT,10,15,color=MUTED)
finish()
# 02
base(True);y=heading('Comece por aqui','Três passos.<br/>Um jeito de trabalhar.','Uma preparação no primeiro uso. Depois, você repete o processo com cada projeto.')
y=step(1,'Baixe e extraia o pacote','Guarde em uma pasta estável e abra essa pasta no Claude Code ou no Codex.',y)
y=step(2,'Organize os materiais','Separe vídeos brutos, referências, manual da marca e áudio. A IA pode criar as pastas.',y)
y=step(3,'Anexe o PDF e faça o pedido','Indique a pasta do projeto, o objetivo e a entrega. A IA verifica as ferramentas e prepara a primeira versão.',y)
y=note('Se o chat não aceitar PDF, informe o caminho do arquivo e peça a leitura do <b>SKILL.md</b>. O PDF orienta; não instala programas nem concede acesso ao disco.',M,y-8)
button('1 · Baixar',M,y-22,186,'#p4',True);button('2 · Organizar',M+202,y-22,186,'#p5');button('3 · Pedir',M+404,y-22,192,'#p6')
finish()
# 03
base();y=heading('Antes de começar','A IA precisa de<br/>uma mesa de trabalho.','Claude e Codex podem seguir a mesma skill. O que muda é o acesso e as ferramentas da sessão.')
for n,t,b in [(1,'Uma IA com acesso à pasta','Use Claude Code ou Codex em um ambiente habilitado. Apenas citar uma pasta no chat não permite lê-la.'),(2,'Python, FFmpeg e FFprobe','Python executa os helpers. FFmpeg processa a mídia e FFprobe confere os arquivos.'),(3,'Recursos opcionais quando necessários','Node.js 22+ para HyperFrames. ASR para transcrição. Conexão e créditos para serviços de geração.')]:
 y=step(n,t,b,y,108)
button('Preparar Claude Code',M,y-5,288,URL['claude'],True);button('Conhecer o Codex',M+308,y-5,288,URL['codex'])
button('Baixar Python',M,y-59,288,URL['python']);button('Baixar FFmpeg',M+308,y-59,288,URL['ffmpeg'])
finish()
# 04
base();y=heading('Uma vez só','Baixe. Extraia.<br/>Abra a pasta.','No GitHub, o botão verde Code permite baixar o projeto como ZIP. O botão abaixo abre o download direto.')
y=step(1,'Baixe o repositório completo','Não salve apenas o PDF. A skill também usa referências, scripts e templates.',y,102)
y=step(2,'Extraia o ZIP','Abra a pasta extraída. O SKILL.md precisa estar junto das pastas scripts e references.',y,102)
y=step(3,'Peça a verificação inicial','Diga à IA para ler SKILL.md, verificar as dependências e preparar projetos/meu-video.',y,102)
y=note('O repositório já contém adaptadores de projeto para Claude e Codex. Para outra pasta ou uma instalação de usuário, siga o tutorial. A instalação não conecta contas externas.',M,y)
button('Baixar ZIP da FEMO',M,y-106,288,URL['zip'],True);button('Tutorial de instalação',M+308,y-106,288,URL['install'])
finish()
# 05
base(True);y=heading('Todo novo projeto','Cada arquivo<br/>no seu lugar.','Uma pasta por cliente ou trabalho. Assim a IA encontra o material certo e preserva os originais.')
panel(M,y,CONTENT,333)
rows=[('01_brutos','Vídeos e áudios originais'),('02_referencias','Exemplos do resultado desejado'),('03_marca','Manual, logo e fontes autorizadas'),('04_audio','Trilhas e efeitos com direito de uso'),('05_projeto','Transcrição, decisões e montagem'),('06_entregas','Prévias e versões finais'),('07_design','Artes e seus arquivos editáveis')]
for i,(a,b) in enumerate(rows):
 yy=y-22-i*43
 para(a,M+20,yy,172,12.5,18,font='InterBold')
 para(b,M+205,yy,CONTENT-229,12,18,color=MUTED)
 if i<6:line(M+20,yy-28,CONTENT-40)
y-=355
y=note('Acrescente <b>briefing.md</b> na raiz do trabalho: marca, público, objetivo, mensagem, formato e referências. A pasta <b>projetos/</b> é ignorada pelo Git para manter os materiais fora do pacote público.',M,y)
button('Ver a estrutura no GitHub',M,y-115,CONTENT,URL['repo'])
finish()
# 06
base();y=heading('Copie e adapte','Seu primeiro pedido<br/>de edição.','Você não precisa descrever comandos técnicos. Precisa apontar os arquivos e explicar o resultado esperado.')
prompt='Leia o guia FEMO AI Studio e o SKILL.md desta pasta.<br/><br/>Meu projeto está em <b>projetos/meu-video</b>. Use os brutos de <b>01_brutos</b>, as referências de <b>02_referencias</b> e a identidade de <b>03_marca</b>.<br/><br/>Edite uma primeira versão em <b>9:16, até 60 segundos</b>, com cortes naturais, fala preservada e legendas legíveis. Verifique as ferramentas e explique qualquer dependência ausente.<br/><br/>Use arquivos locais. Entregue a prévia, a lista de cortes e as legendas para revisão.'
panel(M,y,CONTENT,340);para(prompt,M+24,y-23,CONTENT-48,14,22)
y-=363
para('Com a skill descoberta, você também pode começar por:',M,y,CONTENT,13,19,color=MUTED)
pill('/femo-ai-studio  ·  Claude Code',M,y-38,288);pill('$femo-ai-studio  ·  Codex',M+308,y-38,288)
button('Abrir pedidos prontos para copiar',M,y-99,CONTENT,URL['prompts'],True)
finish()
# 07
base();y=heading('Por dentro da edição','A IA lê, escolhe,<br/>monta e confere.','O processo deixa rastros: arquivos usados, decisões, cortes e versões. Isso permite corrigir e retomar.')
stages=[('01','Inventário','Duração, orientação, áudio, rotação e cor.'),('02','Leitura do conteúdo','Transcrição temporal e inspeção dos planos relevantes.'),('03','Escolha editorial','Tomadas, sequência, pausas e sentido da fala.'),('04','Prévia','Uma versão de revisão antes da entrega definitiva.'),('05','Conferência','Imagem, som, legendas, grafismos e arquivo exportado.')]
for n,t,b in stages:
 para(n,M,y,38,20,24,color=ORANGE,font='InterLight');para(t,M+62,y,CONTENT-62,18,24,font='InterBold');para(b,M+62,y-31,CONTENT-62,12,18,color=MUTED);line(M,y-66,CONTENT);y-=86
button('Conhecer o Video Use',M,y-2,288,URL['videouse']);button('Workflow local FEMO',M+308,y-2,288,URL['video'],True)
finish()
# 08
base(True);y=heading('O acabamento','Legenda acompanha<br/>a fala. Áudio também.','Revisão no tempo certo: o início de uma legenda na origem muda quando a edição muda.')
panel(M,y,CONTENT,145)
para('ORIGEM',M+20,y-19,200,10,15,color=GREEN,font='InterBold');para('00:20 → 00:25',M+20,y-46,240,24,32,font='InterLight')
para('MONTAGEM',M+327,y-19,220,10,15,color=GREEN,font='InterBold');para('00:05 → 00:10',M+327,y-46,240,24,32,font='InterLight')
para('Uma palavra aos 21 segundos da origem aparece aos 6 segundos da montagem.',M+20,y-105,CONTENT-40,12,18,color=MUTED)
y-=175
for t,b in [('Leia e confira','Nomes, números e termos técnicos precisam ser conferidos contra a origem.'),('Ouça as emendas','Um fade pode reduzir clique, mas não corrige uma sílaba cortada.'),('Teste no celular','Mantenha contraste e leitura. Evite áreas cobertas pela interface do aplicativo.')]:
 para(t,M,y,CONTENT,18,23,font='InterBold');para(b,M,y-32,CONTENT,13,20,color=MUTED);y-=92
button('Ver legendas e áudio no workflow',M,y-1,CONTENT,URL['video'],True)
finish()
# 09
base();y=heading('Motion e grafismos','Quando a ideia<br/>pede movimento.','HyperFrames cria composições HTML que podem ser renderizadas como vídeo. A fonte continua editável.')
panel(M,y,CONTENT,177)
tracks=[('Fala original',0,520),('Título',40,150),('Destaque',210,150)]
for i,(label,start,width) in enumerate(tracks):
 yy=y-25-i*46;para(label,M+18,yy,130,10,15,color=MUTED)
 c.setFillColor(HexColor('#31513F'));c.roundRect(M+150,yy-20,420,24,4,fill=1,stroke=0)
 c.setFillColor(HexColor(ORANGE if i==2 else '#62806A'));c.roundRect(M+150+start*.6,yy-20,width*.6,24,4,fill=1,stroke=0)
y-=205
para('Use para títulos, gráficos e chamadas visuais que ajudam a entender a fala. Para a FEMO, movimento discreto e texto curto.',M,y,CONTENT,15,23)
y=note('Um MP4 comum não tem transparência garantida. Peça o vídeo final ou um overlay compatível, além da fonte. A IA precisa conferir versão, dependências e a renderização.',M,y-106)
button('Abrir HyperFrames',M,y-125,288,URL['hyperframes'],True);button('Ler integrações FEMO',M+308,y-125,288,REPO+'/blob/main/references/integracoes.md')
finish()
# 10
base(True);y=heading('Design com as duas IAs','Um briefing que<br/>vira decisão visual.','O Anatomia do Prompt ajuda a organizar o pedido. A FEMO transforma cada campo em um critério verificável.')
fields=[('Papel','Qual trabalho de design a IA vai executar.'),('Contexto','Marca, público, objetivo e mensagem central.'),('Referência','Composição, tipografia e tratamento a observar.'),('Restrições','O que preservar e o que prejudica a peça.'),('Formato','Dimensões, slides, textos e fonte editável.')]
for i,(t,b) in enumerate(fields):
 panel(M,y,CONTENT,65);para(f'{i+1:02}',M+16,y-18,30,15,20,color=GREEN);para(t,M+62,y-13,150,16,20,font='InterBold');para(b,M+223,y-15,CONTENT-244,12,18,color=MUTED);y-=76
para('Comece pela capa ou peça piloto. Depois amplie mantendo o sistema visual e variando a composição.',M,y-5,CONTENT,14,21)
button('Estudar Anatomia do Prompt',M,y-86,288,URL['anatomy'],True);button('Abrir módulo de design',M+308,y-86,288,URL['design'])
finish()
# 11
base();y=heading('Exemplo de briefing','Cinco passos.<br/>Cinco slides.','Design de sobrancelhas para iniciantes: um exemplo didático, sem promessa de renda nem personagem inventada.')
texts=[('1','Prepare sua base','Técnica e cuidados antes da oferta.'),('2','Mostre seu trabalho','Portfólio honesto e fotos autorizadas.'),('3','Explique sua oferta','Serviço, tempo e valor com boa leitura.'),('4','Comece pela sua rede','Apresente o trabalho e facilite contato.'),('5','Cuide de quem chegou','Atendimento, feedback e próximo passo.')]
for i,(n,t,b) in enumerate(texts):
 panel(M,y,CONTENT,64);para(n,M+17,y-17,28,21,25,color=ORANGE);para(t,M+65,y-12,CONTENT-90,16,21,font='InterBold');para(b,M+65,y-37,CONTENT-90,11.5,17,color=MUTED);y-=74
y=note('O tema e o passo 1 dividem a capa; o passo 5 divide o encerramento. A foto da profissional e a referência precisam ser fornecidas. A identidade da cliente deve orientar a peça.',M,y-2)
button('Abrir roteiro e briefing completos',M,y-22,CONTENT,URL['example'],True)
finish()
# 12
base();y=heading('Fidelidade à marca','O estilo precisa<br/>aparecer na execução.','Kit de Marca e referências ajudam. A primeira peça mostra se a composição realmente corresponde ao manual.')
colors=[(GREEN,'#071E18'),(SUPPORT,'#123A2C'),(GREY,'#E5E5E5'),(WHITE,'#FFFFFF'),(ORANGE,'#E35C0A')]
for i,(col,label) in enumerate(colors):
 x=M+i*121;c.setFillColor(HexColor(col));c.roundRect(x,y-66,108,66,5,fill=1,stroke=0);para(label,x,y-78,110,10,14,color=MUTED)
y-=130
para('Para a FEMO',M,y,CONTENT,19,25,font='InterBold');para('Verde sustenta a composição. Laranja pontua. Títulos e apoio têm papéis definidos. Logo original, respiro e leitura vêm antes do efeito.',M,y-39,CONTENT,14,22,color=MUTED)
y-=145
para('Para cada cliente',M,y,CONTENT,19,25,font='InterBold');para('Leia o manual próprio. Use cores, fontes, fotos e linguagem da marca. O visual da documentação FEMO não se transfere automaticamente para seus clientes.',M,y-39,CONTENT,14,22,color=MUTED)
y-=145
y=note('Se a entrega precisa ser Canva editável, use a conexão e um modelo nativo aprovado. HTML, SVG, PNG e PDF têm outras funções e não equivalem ao arquivo Canva.',M,y)
button('Abrir o Canva',M,y-22,288,URL['canva'],True);button('Escolher o formato editável',M+308,y-22,288,URL['design'])
finish()
# 13
base(True);y=heading('Geração opcional','Uma cena de apoio<br/>quando ela faz sentido.','KAIROGEN oferece geração de imagens e vídeos. Isso é uma etapa diferente de montar os seus brutos.')
y=step(1,'Prepare uma intenção visual','Descreva cena, proporção, luz, composição e duração. Evite pedir texto final ou logo dentro de uma imagem quando precisam ser exatos.',y,116)
y=step(2,'Confira a conexão e os créditos','O site anuncia MCP. A ferramenta só pode executar se a conta estiver conectada e a capacidade estiver disponível.',y,116)
y=step(3,'Importe o resultado para o projeto','Sem integração, use o prompt no aplicativo, baixe o arquivo e informe a pasta à IA. Registre origem e direito de uso.',y,116)
y=note('Este pacote não inclui uma conta KAIROGEN nem uma integração autenticada. Não inventa endpoint ou plano. Enviar rostos, vozes ou brutos a um serviço depende de autorização para esse material e destino.',M,y-3)
button('Abrir a KAIROGEN',M,y-22,288,URL['kairo'],True);button('Ver integrações e limites',M+308,y-22,288,REPO+'/blob/main/references/integracoes.md')
finish()
# 14
base();y=heading('Revisão que funciona','Diga onde.<br/>Diga o que mudar.','Uma revisão precisa preserva o que já foi aprovado e reduz retrabalho.')
panel(M,y,CONTENT,172)
para('EXEMPLO DE PEDIDO',M+22,y-22,CONTENT-44,10,14,color=WHITE,font='InterBold')
para('Na versão v001, entre 00:12 e 00:17, mantenha a pausa antes da conclusão e reduza o zoom. No trecho 00:28, corrija a palavra indicada no SRT. Preserve o restante e exporte v002.',M+22,y-58,CONTENT-44,16,25)
y-=207
for t,b in [('Prévia antes da aprovação','Assista e ouça. Confira o conteúdo contra os brutos e as legendas.'),('Nova versão, histórico preservado','Peça para registrar mudanças no project.md e manter a EDL.'),('Entrega com fonte','Vídeo e SRT; artes e seus editáveis. O formato depende do destino combinado.')]:
 para(t,M,y,CONTENT,17,24,font='InterBold');para(b,M,y-32,CONTENT,13,20,color=MUTED);y-=92
button('Abrir pedidos de revisão',M,y-5,CONTENT,URL['prompts'],True)
finish()
# 15
base(True);y=heading('Se algo não funcionar','O próximo passo<br/>precisa ser específico.','A IA deve identificar a dependência real e preservar o trabalho. Uma tentativa não é uma exportação concluída.')
problems=[('A IA não vê a pasta','Abra o projeto em uma sessão com acesso local ou disponibilize os arquivos no ambiente autorizado.'),('Python ou FFmpeg ausente','Peça um diagnóstico. Instale pela fonte oficial e confira o executável encontrado.'),('A skill não aparece','Abra a pasta certa, confira SKILL.md e o escopo de instalação. Reinicie a sessão se necessário.'),('Legenda ou corte estranho','Confira a origem e os tempos. Não corrija só a aparência se o sentido mudou.'),('Fonte, foto ou referência faltando','Forneça o ativo ou combine uma alternativa identificada. Não invente anexos.'),('Serviço pede conta ou créditos','Use o fluxo oficial. Sem conexão, receba o prompt e faça a importação manual.')]
for t,b in problems:
 para(t,M,y,CONTENT,16,22,font='InterBold');para(b,M,y-30,CONTENT,12,18,color=MUTED);line(M,y-76,CONTENT);y-=91
button('Abrir solução de instalação',M,y+2,CONTENT,URL['install'],True)
finish()
# 16
base();y=heading('Seu ponto de partida','Baixe. Organize.<br/>Peça a primeira versão.','Guarde este guia junto do pacote. Os botões abaixo abrem os arquivos e as fontes para continuar.')
links=[('Baixar pacote FEMO','zip'),('Abrir GitHub','repo'),('Pedidos prontos','prompts'),('Pesquisa e fontes','research'),('Claude Code','claude'),('Codex','codex'),('Video Use','videouse'),('HyperFrames','hyperframes'),('Canva','canva'),('KAIROGEN','kairo'),('Anatomia do Prompt','anatomy'),('ASR local opcional','whisper')]
for i,(label,key) in enumerate(links):
 x=M+(i%2)*308;yy=y-(i//2)*54;button(label,x,yy,288,URL[key],primary=(i==0))
y-=351
para('Direção e organização: Agência FEMO.',M,y,CONTENT,14,20,font='InterBold')
y=para('Workflow independente. Video Use, HyperFrames, FFmpeg e demais projetos mantêm sua autoria e licenças. As referências didáticas foram estudadas sem copiar suas páginas ou ativos.',M,y-31,CONTENT,11,17,color=MUTED)
y=para('Identidade orientada pelo manual FEMO fornecido. Esta edição usa Inter; Hagrid Text permanece como fonte oficial de títulos e requer arquivo licenciado para reaplicação. O pacote não a redistribui.',M,y-18,CONTENT,10.5,16,color=MUTED)
para('Revisão: 19 de outubro de 2026. Ferramentas, planos e recursos precisam ser conferidos na sessão e na conta em uso.',M,y-17,CONTENT,10,15,color=MUTED)
finish()
if page!=TOTAL:raise ValueError('Quantidade de páginas incorreta')
c.save()
write=ROOT/'work/pdf/layout.json';write.write_text(json.dumps({'pages':page,'elements':boxes},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pdf':str(OUT),'pages':page,'buttons':sum(b['type']=='button' for b in boxes)},ensure_ascii=False))
