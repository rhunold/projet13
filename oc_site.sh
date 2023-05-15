COMMIT_HASH=$(git rev-parse HEAD) \
&& \
docker build --build-arg COMMIT_HASH=$COMMIT_HASH -t rhunold/image_oc_letting:$COMMIT_HASH . \
&& \
docker push rhunold/image_oc_letting:$COMMIT_HASH \
&& \
docker pull rhunold/image_oc_letting:$COMMIT_HASH \
&& \
docker run --name container_oc_letting -p 8000:8000 rhunold/image_oc_letting:$COMMIT_HASH
