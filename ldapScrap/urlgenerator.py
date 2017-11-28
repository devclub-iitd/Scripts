deps = ['am','bioschool','care','cas','cbme','ces','chemical','chemistry','civil','cse','dbeb','dms','ee','hss','iddc','itmmec','library','maths','mech','nrcvee','physics','polymers','rdat','textile']
classes = ['adjunct','emeritus','exfaculty','faculty','retfaculty','vfaculty']

with open("urls.txt","w") as fl:
    for dep in deps:
        for cl in classes:
            url = "http://ldap1.iitd.ernet.in/LDAP/"+dep+"/"+dep+"_"+cl+".shtml"
            fl.write(url+"\n")


