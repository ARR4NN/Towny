import subprocess
changelogPath = "resources/ChangeLog.txt"
filePath = "./staging/prerelease.txt"
pomPath = "pom.xml"
sponsorPath = "./staging/sponsortable.txt"
currentVersion = "0.0.0.0"
lastFullReleaseVersion = ""
versionList = []
changelog = []
releaseBody = []

def getCurrentVersion():
    from xml.etree import ElementTree as et
    ns = "http://maven.apache.org/POM/4.0.0"
    et.register_namespace('', ns)
    tree = et.ElementTree()
    tree.parse(open(pomPath))
    p = tree.getroot().find("{%s}version" % ns)
    return p.text

def populatePreReleaseList(curVer):
    split = curVer.split(".")
    stringStart = split[0] + "." + split[1] + "." + split[2] + "."
    version = int(split[3])
    for x in range(version):
        versionList.append(stringStart + str(x + 1))
    return stringStart + "0"

def populateChangelog():
    changelogFile = open(changelogPath, "r", encoding="utf-8")
    write = False
    start = versionList[0] + ":"
    while changelogFile:
        line = changelogFile.readline()
        if write == False and line.startswith(start):
            write = True
        if write == True:
            changelog.append(line.replace("\n",""))
        if line == "":
            break
    changelogFile.close()

def addCurrentRelease():
    addLinesToBodyFor(versionList[0])
    addBreak()

def addBreak():
    releaseBody.append("")
    releaseBody.append("----")
    releaseBody.append("")

def addLinesToBodyFor(version):
    append = False
    for line in changelog:
        if append == False and line.startswith(version):
            append = True
            continue
        if append and line.startswith("  "):
            releaseBody.append(line.replace("\n",""))
        if append and line.startswith("  ") == False:
            break
        if line == "":
            break

def addPastReleases():
    releaseBody.append("<details><summary>Cumulative changes since %s</summary>" % lastFullReleaseVersion) 
    versionList.pop(0)
    for versionNumber in versionList:
        releaseBody.append("<details><summary>%s</summary>" % versionNumber)
        releaseBody.append("")
        addLinesToBodyFor(versionNumber)
        releaseBody.append("</details>")
    releaseBody.append("</details>")
    addBreak()

def addSponsorTable():
    sponsortable = open(sponsorPath, "r")
    for line in sponsortable:
        releaseBody.append(line.replace("\n",""))
        if line == "":
            break
    sponsortable.close()
    releaseBody.append("")

def addFooter():
    tableopen = "<table align=center>"
    tableheader = "<th colspan=3> Important Links </th>"
    table1 = "<tr align=center>"
    table2 = "<td><a title=\"How Towny Works\" href=https://github.com/TownyAdvanced/Towny/wiki/How-Towny-Works>How Towny Works</a></td>"
    table3 = "<td><a title=\"Install Guide\" href=https://github.com/TownyAdvanced/Towny/wiki/Installation>Towny Install Guide</a></td>"
    table4 = "<td><a title=\"Updating Towny\" href=https://github.com/TownyAdvanced/Towny/wiki/Updating-Towny>Towny Update Guide</a></td></tr>"
    table5 = "<tr align=center>"
    table6 = "<td><a title=\"Towny Changelog\" href=\"https://raw.githubusercontent.com/TownyAdvanced/Towny/master/resources/ChangeLog.txt\" target=\"_blank\" rel=\"noopener\">Complete Changelog</a> </td>"
    table7 = "<td><a title=\"Default Config Files\" href=\"https://github.com/TownyAdvanced/Towny/wiki/Config-Files\">Default Config Files</a></td>"
    table8 = "<td><a title=\"Commands/Permissions/Placeholders\" href=\"https://github.com/TownyAdvanced/Towny/wiki/Reference\">Commands/Permissions<br>Placeholders</a></td></tr>"
    tableclose = "</table>"
    footer = "### ⏬ Download available as a .jar file in the Assets section below:"
    releasefooter = [tableopen, tableheader, table1, table2, table3, table4, table5, table6, table7, table8, tableclose, "", footer]
    for line in releasefooter:
        releaseBody.append(line)

def buildBody():
    addCurrentRelease()
    if currentVersion.endswith(".1") == False:
        addPastReleases()
    addSponsorTable()
    addFooter()

def writeBody():
    file = open(filePath, 'w', encoding="utf-8")
    for line in releaseBody:
        file.writelines(line + "\n")
    file.close

def echoCurrVer():
    subprocess.call(' echo "CURR_VER=' + currentVersion + '" >> $GITHUB_ENV', shell=True)
    
currentVersion = getCurrentVersion()
lastFullReleaseVersion = populatePreReleaseList(currentVersion)
populateChangelog()
versionList.reverse()
buildBody()
writeBody()
echoCurrVer()
