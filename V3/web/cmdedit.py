#!/usr/bin/python


import io
import os
import json
from time import time
from flask import Flask, render_template, request, jsonify
from wtforms import Form, StringField, TextAreaField, validators, StringField, SubmitField

#DEBUG = True
app = Flask(__name__)
#app.config.from_object(__name__)
#app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class cmdForm(Form):
    #ID = StringField("id", validators=[validators.Regexp("/[0:9]+/",message = "number required")])
    #ID = StringField("id", validators=[validators.Regexp("/[0:9]+/",message = "number required")])
    header = StringField()
    commmand = TextAreaField()
    tags = TextAreaField()
    source = StringField()


@app.route('/', methods =['GET','POST'])
def cmd():
    
    form = cmdForm(request.form)
    print((form.errors))
    print((jsonify(form.errors)))


    with open("../cmd.json","r") as f:
        d=json.load(f)
    f.close()
    
    if request.method == 'POST':

        #backup cmd.json
        datename = str(time())
        print(datename)
        os.system("cp ../cmd.json ../backup/" + datename + ".json")
        s= [{}] 
        s[0]["id"] = int(request.form["id"])
        s[0]["header"] = request.form["header"]
        s[0]["command"] = request.form["command"]
        s[0]["tags"] = request.form["tags"]
        s[0]["source"] = request.form["source"]

        found = False
        
        for c in d["commands"]:
            if c["id"]== int(request.form["id"]):
                #c=s[0] does not work
                c["header"]=request.form["header"]
                c["command"] = request.form["command"]
                c["tags"] = request.form["tags"]
                c["source"] = request.form["source"]
                found=True
                break
        if not found:
            d["commands"].extend(s)
       

        #with io.open('filename', 'w', encoding='utf8') as json_file:
        #json.dump(u"xxx", json_file, ensure_ascii=False)

        with open("../cmd.json","w") as f:
            #pprint(d)
            json.dump(d,f)
        f.close()


    #    print jsonify(request.form["tags"])
    #    print (request.form["tags"])
    #    if form.validate():
    #        flash ("got it")
    #    else:
    #        flash ("nope")

    # get the next unused id's
    usedIDs=[]
    freeIDs=[]
    for c in d["commands"]:
        usedIDs.append(c["id"])
    for i in range(1,10000):
        if i not in usedIDs:
            freeIDs.append(i)
            if len(freeIDs)> 4:
                break

#for c in d["commands"]:
    #    for i in range(10000):
    #        if i not in d["commands"][0]["id"]:
    #            freeIDs.append(i)
    #            if len(freeIDs) > 4:
    #                break

    commands = d["commands"]
    return render_template("cmd.html", form=form, commands=commands, freeIDs = freeIDs)

