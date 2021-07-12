Pythonic Function Server

This repository contains code enabling a python-based communication with IAV Scene Suite.

Scene Suite features a xml-based interface. Below you can find some messages that serve as examples:

From Scene Suite to the server:
```xml
<NetworkData xmlns="sop.iav.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" createdBySceneSuiteVersion="0.18.0" dateOfCreation="2021-03-15T11:33:46" sceneID="scn.example" timeResolution="0.06">
    <MetaData NumOfFrames="68" NumOfMovements="2" SceneId="scn.example" TimeResolution="0.06" external="">
        <MovementData channel="chn.ego" id="mov.ego" name="obj.Mercedes_S500_lang"/>
        <MovementData channel="chn.object" id="mov.object" name="obj.Audi_Q7_01_BJ2014"/>
    </MetaData>
    <Frame isOwn="true" mountedSensorID="mns.mountedSensor" objectID="mov.ego (obj.Mercedes_S500_lang)" time="0.0" xsi:type="ObjectListSensorFrame"/>
</NetworkData>
```

From the server to Scene Suite:
```xml
<ServerResponse>
    <Channel id="chn.ego">
        <Parameter xsi:type="Acceleration" value="0.0" />
        <Parameter xsi:type="FunctionValue">
            <Expression expressionString="TTC=-10.0" />
            <Expression expressionString="vRel=-0.0" />
            <Expression expressionString="timegap=10.0" />
            <Expression expressionString="dist=3.5" />
            <Expression expressionString="minDist=-999.9" />
            <Expression expressionString="minTTC=-1.0E9" />
            <Expression expressionString="crash=0.0" />
            <Expression expressionString="target=0.0" />
        </Parameter>
    </Channel>
</ServerResponse>
```