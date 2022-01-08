import os


def check_requirements():

    print("Checking for requirements...")
    print("sudo apt-get update && sudo apt-get upgrade")
    os.system("sudo apt-get update && sudo apt-get upgrade")
    # uncomment line below if on mac OSX:
    # sudo port sync && sudo port upgrade outdated
    opam1 = "opam update"
    print(opam1)
    os.system(opam1)

    opam2 = "opam upgrade"
    print(opam2)
    os.system(opam2)

    pip_g = "pip3 install grew --upgrade"
    print(pip_g)
    os.system(pip_g)

    pip_r = "pip3 install -r requirements.txt --upgrade"
    print(pip_r)
    os.system(pip_r)
    try:
        import pyconll
    except ImportError:
        os.system("pip3 install pyconll")

    try:
        import pandas
    except ImportError:
        os.system("pip3 install pandas")


if __name__ == "__main__":

    check_requirements()
