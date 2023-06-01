import maya.cmds as cmds

startTime = cmds.playbackOptions(q=True, min=True)
endTime = cmds.playbackOptions(q=True, max=True)
sel = cmds.ls(sl=True)
localScale = 10

print(startTime, endTime)
print("Selected objects:")
for s in sel:
    print(s)

if len(sel) == 0:
    cmds.confirmDialog(m="Select something")
else:
    for item in sel:
        name = item+"_temp_loc"
        loc = cmds.spaceLocator(n=name)[0]

        cmds.setAttr("{0}.localScaleX".format(loc), localScale)
        cmds.setAttr("{0}.localScaleY".format(loc), localScale)
        cmds.setAttr("{0}.localScaleZ".format(loc), localScale)

        cmds.pointConstraint(item, name)
        cmds.orientConstraint(item, name)

        response = cmds.confirmDialog(title="Confirmation", m="Want to get it baked?", b=["Yeah", "Nah"], db="Nah",
                                      cb="Nah", ds="Nah")

        if response == "Yeah":
            cmds.select(name)
            cmds.bakeResults(simulation=True, time=(startTime, endTime), sampleBy=1, disableImplicitControl=True,
                             preserveOutsideKeys=True, sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False,
                             removeBakedAnimFromLayer=False, bakeOnOverrideLayer=False, minimizeRotation=True,
                             controlPoints=False)
            cmds.delete(sc=True)
            cmds.filterCurve()
            cmds.delete(cn=True)
        else:
            cmds.delete(name, cn=True)
