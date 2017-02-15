from minigame import *

def testSearchPlay():
    try:
        s=Search()
        s.play(randomPolicy)
        return "No exceptions"
    except Exception as e:
        print "Failure in testSearchPlay"
        raise e


if __name__ == "__main__":
    print(testSearchPlay())