# Makefile guide

We use Makefiles extensively to help make the developer’s life simpler and more efficient.
Here are the key targets for this `Makefile`.

- run: Run the app in development mode.

- run-prod: Run the app in production mode.

- `build``: Build the app.

- `clean``: Clean the build environment.

- `all``: clean and build.

- `test`: Run `jest` testing on the app

- `install-gcloud-cli`: convenient target to set up your GCloud CLI environment, so you can deploy these examples to your Gcloud-hosted space.

- `gcloud-create`: create the GCloud project if it doesn’t exist.

- `gcloud-enable-cloudbuild`: enable the Cloud-Build service for the GCloud project.

- `gcloud-log`: tail the logs for the GCloud project.

## Links

- [README](README.md)
