DC := docker
#This is the outside port we can access docker from
HOSTPORT ?= 3015
#This is the port docker will expose
DCPORT ?= 8000
#This is the image name
IMAGENAME ?= example_image
#The arguments to build a docker image
DCBUILDARGS := build -t 
#The arguments to run a docker image.
DCRUNARGS := run
#The Service Key
SERVICEKEY := $(serviceKey)
#The Config Key
CONFIGKEY := $(configKey)

#creats a docker image and runs it
all: create_image run_image

#creats a docker image
create_image:
	$(DC) $(DCBUILDARGS) $(IMAGENAME) .

#runs a docker image
run_image:
	$(DC) $(DCRUNARGS) -e PORT=$(DCPORT) \
	 -e serviceKey=$(SERVICEKEY) \
	 -e configKey=$(CONFIGKEY) \
	 -p $(HOSTPORT):$(DCPORT) \
	 -d $(IMAGENAME)

#stops all running containers and removes them
clean:
	$(DC) kill $(shell $(DC) ps -q)
	$(DC) rm $(shell $(DC) ps -a -q)
	$(DC) rmi $(shell $(DC) images -f "dangling=true" -q)
#stops all running containers, removes them, and also the created images.

cleanContainer:
	$(DC) kill $(shell $(DC) ps -q)
	$(DC) rm $(shell $(DC) ps -a -q)

cleanImages:
	$(DC) rmi $(shell $(DC) images -a -q)

cclean: cleanContainer cleanImages
	
	
	