from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path(__file__).parent
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1000,'height':680},device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((out/'Simple House.html').as_uri())
    page.wait_for_function('window.houseTest && houseTest.renderer.info.render.calls > 0')
    initial=page.evaluate('houseTest.getState()')
    page.mouse.move(450,280);page.mouse.down();page.mouse.move(550,310,steps=10);page.mouse.up()
    assert page.evaluate('houseTest.getState().theta')!=initial['theta']
    page.mouse.wheel(0,-200);page.wait_for_timeout(100)
    assert page.evaluate('houseTest.getState().scale')<initial['scale']
    page.click('#front');assert page.evaluate('houseTest.getState().theta')==0
    page.click('#spin');assert page.get_attribute('#spin','aria-pressed')=='true'
    page.wait_for_timeout(100);assert page.evaluate('houseTest.getState().theta')>0
    page.click('#spin');page.click('#reset');page.wait_for_timeout(300)
    with page.expect_download() as info:page.click('#download')
    download=info.value
    assert download.suggested_filename=='Simple House.glb'
    assert Path(download.path()).read_bytes()==(out/'Simple House.glb').read_bytes()
    page.screenshot(path=str(out/'Simple House.png'))
    page.set_viewport_size({'width':390,'height':640});page.click('#reset');page.wait_for_timeout(100)
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path=str(out/'Simple House mobile.png'))
    assert not errors, errors
    print(json.dumps({'browser':'Edge','parts_rendered':page.evaluate('houseTest.parts'),'render_calls':page.evaluate('houseTest.renderer.info.render.calls'),'tests':['drag orbit','wheel zoom','front view','auto rotate','reset','GLB download byte match','mobile no horizontal overflow'],'page_errors':errors}))
    browser.close()
