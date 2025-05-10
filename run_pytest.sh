set -x

podman build  -t my_image -f Dockerfile .

podman run --rm -v "$(pwd):/app"  -t my_image pytest  test_main.py --myarg nisse

