import dominate, datetime
from dominate.tags import *

def getHTML(name, number, msgList, filename):
    dateCount = smsCount = mmsCount = msgCount = 1
    msgId = ""

    stylesheetName = "style.css"
    numberStr = "(" + (str(number)[0:3]) + ") " + (str(number)[3:6]) + "-" + (str(number)[6:10])
    docTitle = name + " at " + numberStr
    #print(docTitle)

    doc = dominate.document(title=docTitle)

    with doc.head:
        link(rel="stylesheet", href=stylesheetName)
        meta(charset="UTF-8")
    
    with doc.body:
        with header():
            h3(name, id="contact_name")
            h6(numberStr, id="contact_number")

    with doc.body.add(div(id="message_content")) as d:
        dateVals = (msgList[len(msgList) - 1])[0].split("-")
        currDate = datetime.date(int(dateVals[2]), int(dateVals[0]), int(dateVals[1]))
        for (date, status, msgType, val) in reversed(msgList):
            dateVals = date.split("-")
            newDate = datetime.date(int(dateVals[2]), int(dateVals[0]), int(dateVals[1]))

            with d.add(div(cls="msg_block")):
                    if ((currDate != newDate) or (msgCount == 1)):
                        p(str(newDate), cls="date")
                    else:
                        currDate = newDate

                    if (status == "R"):
                        if (msgType == "SMS"):
                            msgId = msgType + "_" + str(smsCount)
                            p(val, id=msgId, cls="r_message")
                            msgCount += 1
                            smsCount += 1
                        elif (msgType == "MMS"):
                            msgId = msgType + "_" + str(mmsCount)
                            img(src=val, width="500", height="250", cls="r_message MMS", id="image")
                            msgCount += 1
                            mmsCount += 1
                    else:
                        if (msgType == "SMS"):
                            msgId = msgType + "_" + str(smsCount)
                            p(val, id=msgId, cls="s_message")
                            msgCount += 1
                            smsCount += 1
                        elif (msgType == "MMS"):
                            msgId = msgType + "_" + str(mmsCount)
                            img(src=val, width="500", height="250", cls="r_message MMS", id="image")
                            msgCount += 1
                            mmsCount += 1
                

    with open(filename, "w") as fp:
        print(doc, file=fp)

def main():
    msgList = [('01152018', 'R', 'SMS', 'Eh, wouldn=E2=80=99t hurt'), ('01122018', 'S', 'SMS', 'Also should I review calc 3 over break to get ready for 380?'), ('01122018', 'S', 'SMS', 'Hey do you have PDFs of the 303/350/380 textbooks '), ('12162017', 'S', 'SMS', '=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0==9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F==91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91==80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80'), ('12162017', 'S', 'SMS', '=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0==9F=91=80'), ('12162017', 'S', 'SMS', 'Wya'), ('12162017', 'R', 'SMS', 'It=E2=80=99s Kool =F0=9F=91=8C=F0=9F=8F=BE'), ('12162017', 'S', 'MMS', 'Images/Elliot_Tapscott_3015028527_img_1.jpg'), ('12162017', 'S', 'SMS', "I didn't take very good notes during the review sorry haha"), ('12162017', 'S', 'MMS', 'Images/Elliot_Tapscott_3015028527_img_2.jpg'), ('12162017', 'S', 'SMS', '=2E=2E=2Eand 7')]

    msgList01 = [('01-15-2018', 'R', 'SMS', 'Eh, wouldn=E2=80=99t hurt'), ('01-12-2018', 'S', 'SMS', 'Also should I review calc 3 over break to get ready for 380?'), ('01-12-2018', 'S', 'SMS', 'Hey do you have PDFs of the 303/350/380 textbooks '), ('12-16-2017', 'S', 'SMS', '=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0==9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F==91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91==80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80'), ('12-16-2017', 'S', 'SMS', '=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0=9F=91=80=F0==9F=91=80'), ('12-16-2017', 'S', 'SMS', 'Wya'), ('12-16-2017', 'R', 'SMS', 'It=E2=80=99s Kool =F0=9F=91=8C=F0=9F=8F=BE'), ('12-16-2017', 'S', 'MMS', 'Images/Elliot_Tapscott_3015028527_img_1.jpg'), ('12-16-2017', 'S', 'SMS', "I didn't take very good notes during the review sorry haha"), ('12-16-2017', 'S', 'MMS', 'Images/Elliot_Tapscott_3015028527_img_2.jpg'), ('12-16-2017', 'S', 'SMS', '=2E=2E=2Eand 7')]

    filename = "Elliot_Tapscott_3015028527_0.html"
    getHTML("Elliott Tapscott", 3015028527, msgList01, filename)

if __name__ == "__main__":
    main()