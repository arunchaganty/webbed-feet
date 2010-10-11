# Abstraction of a game and all it's aspects

class Game:
    @classmethod
    def submissionHook(cls, uploaded_file):
        return uploaded_file

    @classmethod
    def runHook(cls, player1, player2):
        return 0

    @classmethod
    def scoreHook(cls, output):
        if score.isdigit():
            score = int(score)
            # Make any modifications
            return score
        else:
            # Handle various error codes
            return 0

