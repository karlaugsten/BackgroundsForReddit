#!/usr/bin/env bash
# Installs dependencies for BackgroundsForReddit.

# Check if user has brew installed.
# Prompt user if they want to install homebrew.
# This is necessary for installing python and pip through terminal.
promptBrewInstall () {
    brewMessage=`which brew`

    # Prompt user if they want to install homebrew.
    if [ "$brewMessage" = "brew not found" ]; then
        echo "Homebrew does not seem to be installed."
        read -p "Would you like to install the homebrew package manager? (y/n)" yn
        case $yn in
            [Yy]* ) ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" ;
                break;;
            * ) echo "Homebrew is necessary for installing Python and pip."
                exit;;
        esac
    fi
}

# Install Python and app dependencies through homebrew and pip.
installDependencies () {
    read -p "Would you like to install Python, pip, and other dependencies? (y/n)" yn
    case $yn in
        [Yy]* ) echo "Installing Python and pip."
            brew install python # Installs Python and pip
            echo "Python and pip installed."
            pip install praw pyobjc-core pyobjc rumps flufl.enum pillow urllib3 py2app
            echo "Dependencies installed." ;;
        * ) echo "Dependencies are necessary to develop the application."
            exit ;;
    esac 
}

# Run commands.
promptBrewInstall
installDependencies

