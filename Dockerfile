FROM python:3.7-alpine as builder

# Install build-base to allow for compilation of the profiling agent.
RUN apk add --update --no-cache build-base

# Compile the profiling agent, generating wheels for it.
RUN pip3 wheel --wheel-dir=/tmp/wheels google-cloud-profiler


FROM python:3.7-alpine

# Copy over the directory containing wheels for the profiling agent.
COPY --from=builder /tmp/wheels /tmp/wheels

# Install the profiling agent.
RUN pip3 install --no-index --find-links=/tmp/wheels google-cloud-profiler

# Install any other required modules or dependencies, and copy an app which
# enables the profiler as described in "Enable the profiler in your
# application".
# COPY ./bench.py . #  TODO

# Run the application when the docker image is run, using either CMD (as is done
# here) or ENTRYPOINT.
# CMD python3 -u bench.py   # TODO