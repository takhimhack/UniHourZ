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
DCRUNARGS := run -e PORT=$(DCPORT) -p $(HOSTPORT):$(DCPORT) -d 

#creats a docker image and runs it
all: create_image run_image

#creats a docker image
create_image:
	$(DC) $(DCBUILDARGS) $(IMAGENAME) .

#runs a docker image
run_image:
	$(DC) $(DCRUNARGS) -d $(IMAGENAME)

#stops all running containers, removes them, and also all images.
clean:
	$(DC) kill $(shell $(DC) ps -q)
	$(DC) rm $(shell $(DC) ps -a -q)
	$(DC) rmi $(shell $(DC) images -q)