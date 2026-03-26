# calculates the average of the 5 marks and returns the avg
def calcAverage(gradeSum):
    avg = gradeSum / 5
    return avg


# assigns a grade symbol to the avg mark
def determineGrade(avg):
    if avg >= 90 and not avg > 100:
        return 'A'
    elif avg >= 80:
        return 'B'
    elif avg >= 70:
        return 'C'
    elif avg >= 60:
        return 'D'
    else:
        return 'F'


# main program logic
def main():
    mark = 0
    for i in range(5):
        mark += int(input('Please enter your test score: '))

    print(f'Your test average was {calcAverage(mark)}')
    print(f'Letter grade: {determineGrade(calcAverage(mark))}')


main()
