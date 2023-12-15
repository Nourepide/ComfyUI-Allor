@echo off

for /f %%i in ('git rev-parse --abbrev-ref HEAD') do set branch=%%i
for /f "delims=" %%i in ('git log -1 --pretty=%%B') do set commit=%%i
for /f %%i in ('git rev-parse --short HEAD') do set hex=%%i

echo {\"branch\": \"%branch%\", \"commit\": \"%commit%\", \"hex\": \"%hex%\"} > info.json
