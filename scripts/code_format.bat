@ECHO OFF
REM previous line reduces outputs to relevant ones

ECHO [92mINFO: activating environment and setting proxy[0m
CALL activate compass

ECHO [92mINFO: starting code styling via black[0m
CALL black %~dp0\.. -l 79

REM avoid terminal closing so that user can view output
PAUSE