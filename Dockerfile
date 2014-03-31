FROM ubuntu

# Requirements
RUN apt-get install -y wget

# RackOS specifics
RUN echo "deb http://pkg.ohthree.com/ onion main" >> /etc/apt/sources.list
RUN echo "deb http://pkg.ohthree.com/ onion-unstable main" >> /etc/apt/sources.list
RUN wget -q -O - http://pkg.ohthree.com/signing.gpg.key | apt-key add -

# Get Dorap using a version specific reference
RUN apt-get update && apt-get install dorap=0.0.10 -y

# Cleanup
RUN apt-get purge wget -y

# Expose components
ENTRYPOINT ["dorap"]
EXPOSE 8080
