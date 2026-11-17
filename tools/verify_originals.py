"""Verify original-question coverage, image files, and rendered desktop/mobile UI."""
import asyncio,json,re,sys
from pathlib import Path
from collections import defaultdict
from lxml import html
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_bundle import build
from cdp import Browser
from apply_originals import load_manifest
ROOT=Path(__file__).resolve().parents[1]
READY="document.querySelector('.original-source') && document.fonts.status==='loaded'"
async def main():
    build();data=load_manifest()
    pages=[];total=0;unique=set()
    for chapter in sorted({v['chapter'] for v in data.values()}):
        base=ROOT/'subjects'/chapter;config=json.loads((base/'chapter.json').read_text(encoding='utf-8'))
        exam=html.fromstring((base/'exam.html').read_text(encoding='utf-8'))
        for sec in config['sections']:
            path=base/'sections'/sec['file'];tree=html.fromstring(path.read_text(encoding='utf-8'))
            cards=tree.xpath('//div[@class="problem"]')
            if not cards:continue
            pages.append((chapter,sec['id'],cards[0].get('id'),len(cards)))
            for card in cards:
                pid=card.get('id');key=chapter+'/'+pid
                assert key not in unique,key
                unique.add(key);total+=1
                original=card.xpath('.//section[@class="original-source"]');assert len(original)==1,key
                side=exam.xpath(f'//article[@data-exam-id="{pid}"]//section[@class="original-source"]');assert len(side)==1,key
                assert html.tostring(original[0])==html.tostring(side[0]),key
                assert original[0].get('data-original-id')==pid,key
                for im in data[key]['images']:
                    p=ROOT/im['src'];assert p.is_file(),p
                    with Image.open(p) as image:assert image.size==(im['width'],im['height']),p
    assert unique==set(data),(len(unique),len(data))
    print(f'Static: {total} cards + {total} matching sidebars; all images verified',flush=True)
    report=[];shots=ROOT/'tools/reports/originals';shots.mkdir(exist_ok=True)
    async with Browser(1280,1000,port=9560) as browser:
        await browser.send('Emulation.setDeviceMetricsOverride',width=1280,height=1000,deviceScaleFactor=1,mobile=False)
        for width in [1280,390]:
            await browser.send('Emulation.setDeviceMetricsOverride',width=width,height=1000,deviceScaleFactor=1,mobile=False)
            for chapter,section,first,count in pages:
                s,c=chapter.split('/');url=(ROOT/'chapter.html').as_uri()+f'?s={s}&c={c}&p={section}'
                await browser.goto(url,ready_js=f"!!document.getElementById({json.dumps(first)}) && document.fonts.status==='loaded'")
                result=await browser.eval("""(async()=>{
                  const root=document.querySelector('#reading');
                  root.querySelectorAll('.original-scan').forEach(d=>d.open=true);
                  const imgs=[...root.querySelectorAll('.original-image')];
                  imgs.forEach(i=>i.loading='eager');
                  const loaded=await Promise.all(imgs.map(i=>i.decode().then(()=>true,()=>false)));
                  await new Promise(r=>setTimeout(r,150));
                  return {cards:root.querySelectorAll('.problem').length,originals:root.querySelectorAll('.original-source').length,
                    badImages:loaded.filter(x=>!x).length,mathErrors:root.querySelectorAll('.original-source .katex-error').length,
                    horizontalOverflow:document.documentElement.scrollWidth>document.documentElement.clientWidth+1};
                })()""")
                assert result['cards']==result['originals']==count,(chapter,section,width,result)
                assert not result['badImages'] and not result['mathErrors'] and not result['horizontalOverflow'],(chapter,section,width,result)
                await browser.eval("document.querySelectorAll('.original-scan').forEach(d=>d.open=false)")
                if section in ['s01','s05','s07'] and chapter in ['modern/ch01','mechanics/ch01','thermal/ch02']:
                    await browser.eval(f"document.getElementById({json.dumps(first)}).scrollIntoView()")
                    (shots/f'{s}-{c}-{section}-{width}.png').write_bytes(await browser.screenshot(fmt='png'))
                await browser.eval("document.querySelector('.problem .exam-btn').click()")
                await asyncio.sleep(.1)
                sidebar=await browser.eval("({originals:document.querySelectorAll('.exam-sidebar .original-source').length,errors:document.querySelectorAll('.exam-sidebar .original-source .katex-error').length})")
                assert sidebar=={'originals':1,'errors':0},sidebar
                report.append(dict(chapter=chapter,section=section,width=width,**result))
            print(f'Rendered: {len(pages)} sections at {width}px; images, math, width and sidebars OK',flush=True)
    (shots/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('ORIGINAL QUESTIONS OK',flush=True)
if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');asyncio.run(main())
