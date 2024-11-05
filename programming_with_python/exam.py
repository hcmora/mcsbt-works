words = ["python", "programming", "challenge"]

result = ""


for word in words:

  # Modification goes here

    # result += ''.join([char.upper() if i %
    #                    2 != 0 else char for i, char in enumerate(word)])

    # result += word[::2].upper() + word[1::2]

    result += ''.join([char.lower() if i % 2 != 0 else char.upper()
                       for i, char in enumerate(word)])


print(result)
