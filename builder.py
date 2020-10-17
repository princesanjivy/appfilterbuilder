# princesanjivy
import os, sys, argparse
from bs4 import BeautifulSoup

ref_xml=open("template.xml", "r")
l=ref_xml.readlines()
avail_apps=sorted({app[app.find("drawable")+len("drawable")+2 : app.rfind('"')]for app in l if "drawable" in app})
    
def listapps():
    for i, app in enumerate(avail_apps):
        print(i+1, app)

def genappfilter(path): #keep only icons(png) in this folder
    appfilter_contents='<?xml version="1.0" encoding="UTF-8"?><resources><scale factor="1"/>XXX</resources>'
    appmap_contents='<?xml version="1.0" encoding="UTF-8"?><appmap>XXX</appmap>'
    con="";cont=""

    applist=os.listdir(path)
    apps=sorted({app.replace(".png", '')for app in applist if ".png" in app})
    print("\nfound %d apps"%len(apps))
    
    if len(apps) >= 1:
        print("%d app(s) doesn't have source in template.xml"%len([1 for app in apps if app not in avail_apps]))

        for app in apps:
            con+="<!-- "+app.title()+" -->\n";cont+="<!-- "+app.title()+" -->\n"
            for j in l:
                if "drawable" in j:
                    name=j[j.find("drawable")+len("drawable")+2 : j.rfind('"')]

                    if name == app:
                        con+=j
                        if 'component="ComponentInfo{' in j:
                            j=j.replace('component="ComponentInfo{', 'class="')
                            j=j.replace('}"', '"')
                            j=j.replace("drawable", "name")

                            cont+=j

            con+="\n";cont+="\n"
        
        package_name=input("app package name: ")
        icon_pack_name=input("icon pack name: ")

        appfilter=open("appfilter.xml", "w")     #appfilter.xml
        appmap=open("appmap.xml", "w")     #appmap.xml

        #adding iconpack's app

        con+="<!-- "+icon_pack_name.title()+" -->\n"
        con+='<item component="ComponentInfo{'+package_name+'/'+package_name+'.activities.SplashActivity}" drawable="'+icon_pack_name+'"/>\n'
        con+='<item component="ComponentInfo{'+package_name+'/'+package_name+'.activities.StartActivity}" drawable="'+icon_pack_name+'"/>\n'

        appfilter_contents=appfilter_contents.replace("XXX", con)
        bs=BeautifulSoup(appfilter_contents, 'xml')
        appfilter.write(bs.prettify())

        print("\nappfilter.xml generated!")
        appfilter.close()

        cont+="<!-- "+icon_pack_name.title()+" -->\n"
        cont+='<item class="'+package_name+'/'+package_name+'.activities.SplashActivity" name="'+icon_pack_name+'"/>\n'
        cont+='<item class="'+package_name+'/'+package_name+'.activities.StartActivity" name="'+icon_pack_name+'"/>\n'

        appmap_contents=appmap_contents.replace("XXX", cont)
        bs=BeautifulSoup(appmap_contents, 'xml')
        appmap.write(bs.prettify())

        print("appmap.xml generated!")
        appmap.close()


parser=argparse.ArgumentParser(description="A python script for generating appfilter.xml and appmap.xml files")
parser.add_argument("-l", "--list-apps", action='store_true', help="list all available apps")
parser.add_argument("-g", "--generate-appfilter", help="generates appfilter.xml & appmap.xml file for given path containing app icons")
parser.add_argument("-c", "--check", help="check whether app is present in template.xml")


args=parser.parse_args()

if len(sys.argv) <= 1:
    exit()
else:
    if args.list_apps:
        listapps()
    if args.generate_appfilter is not None:
        genappfilter(args.generate_appfilter)
    if args.check is not None:
        print(args.check in avail_apps)

print("💙")
