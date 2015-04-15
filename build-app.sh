#/usr/bin/env bash
# Builds the .app executable if all of the dependencies are available.

declare -a pipdependencies=("praw" "pyobjc-core" "pyobjc" "rumps" "flufl.enum"
"Pillow" "urllib3" "py2app")

# Checks if all pip dependencies are satisfied.
checkPipDependencies () {
    dependencies=`pip list`
    for dep in "${pipdependencies[@]}"; do
        if [[ ! "$dependencies" == *"$dep"* ]]; then
            echo "Missing dependencies, please run './developer-setup.sh'"
            exit;
        fi
    done
}

createApp () {
    echo "Creating .app executable file."
    python setup.py py2app -A
    echo "BackgroundsForReddit.app file created."
}

checkPipDependencies
createApp
