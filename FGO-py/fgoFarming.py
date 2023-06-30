# 这里是一坨屎
# 原本为了这个收菜要重构整个fpy结构的,但是这几天先忙pponnxcr了,没来得及
# 所以先拉这一坨,反正只会用20天(

import numpy,re
from functools import reduce
import fgoDevice
from fgoDetect import *
from fgoSchedule import *
from fgoLogging import getLogger,logit

logger=getLogger("Farming")

priority={
    '野原':2,
    '森林':1,
    '山岳':9,
}

def farming():
    if Detect.region!='CN':return 0
    assert Detect().isMainInterface()
    fgoDevice.device.perform('\x08',(1000,))
    while not Detect(.2).isMainInterface():pass
    fgoDevice.device.perform('\xBA',(1000,))

    fgoDevice.device.touch((1190,200))
    schedule.sleep(.5)
    for _ in range(10):
        fgoDevice.device.touch((548,638))
        schedule.sleep(.5)

    commissions=set()
    remain=21600 # 6 hours
    length=0
    while not Detect(.5)._isListEnd((1261,608)):
        img=Detect.cache._crop((717,239,1111,600))
        ocr=OCR.ZH.detect_and_ocr(img)
        for res in ocr:
            text=res.ocr_text
            if '归还' in text or '还需' in text:
                logger.info(f'Running: {text}')
                text=text.replace('：',':').replace('::',':')
                m=re.search(r'(\d?\d):(\d\d):(\d\d)',text)
                if m is None:
                    logger.warning(f'OCR failed: {text}')
                    continue
                remain=min(remain,reduce(lambda x,y:x*60+y,(int(i)for i in m.groups())))
                continue
            if '远征' in text:
                commissions.add(text[3:-1])
                continue
        fgoDevice.device.swipe((800,600,800,300))
        length+=1
    commissions=sorted(commissions,key=lambda x:priority.get(x,999))
    logger.info(f'Commission: {commissions}')
    while commissions:
        commission=commissions.pop(0)
        for _ in range(length+2):
            fgoDevice.device.swipe((800,300,800,600))
            schedule.sleep(.5)
        while not Detect(.5)._isListEnd((1261,608)):
            img=Detect.cache._crop((717,239,1111,600))
            ocr=OCR.ZH.detect_and_ocr(img)
            for res in ocr:
                text=res.ocr_text
                box=res.box
                if commission in text:
                    break
            else:
                fgoDevice.device.swipe((800,600,800,300))
                continue
            break
        fgoDevice.device.touch(numpy.mean(box,axis=0).astype(int)+numpy.array([717,239],dtype=int))
        Detect(.5)
        dogs=[
            ' '.join(j.ocr_text for j in OCR.ZH.detect_and_ocr(Detect.cache._crop((142+125*i,226,263+125*i,360))))
            for i in range(8)
        ]
        logger.info(f'Dogs: {dogs}')
        dogs=[
            (
                (192+125*i,276),
                '相性佳'in j or '减少' in j
            )
            for i,j in enumerate(dogs)
            if '必要' in j and '远征' not in j
        ]
        if not dogs:
            fgoDevice.device.touch((438,616))
            schedule.sleep(.3)
            break
        dog=([i[0]for i in dogs if i[1]]+[i[0]for i in dogs if not i[1]])[0]
        fgoDevice.device.touch(dog)
        schedule.sleep(.3)
        fgoDevice.device.touch((840,616))
        schedule.sleep(.5)
        for _ in range(5):
            fgoDevice.device.touch((548,638))
            schedule.sleep(.5)
    fgoDevice.device.perform('\x67',(2000,))
    while not Detect(.2).isMainInterface():pass
    logger.info(f'Remain: {divmod(remain,60)}')
    return remain

if __name__=='__main__':
    fgoDevice.device=fgoDevice.Device('127.0.0.1:13833')
    farming()
