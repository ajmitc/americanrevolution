#!/bin/bash

./consul agent -dev -ui -datacenter zone1 -node host1

# To exit consul, run:
# > ./consul leave
