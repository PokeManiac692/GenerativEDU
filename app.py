from flask import Flask, render_template, redirect, request, session, abort
import os
import cohere
from cohere.classify import Example

app = Flask(__name__)
apiKey = os.environ.get('COHERE_API_KEY')


def build_prompt(list1):
    og_list = list1
    stringPrompt = ""
    for item in list1:
        stringPrompt += item + "\n"

    model = 'Lesson Title: Binary Numbers\nSubject: Computer Science\nObjectives: Explain how the position of each binary digit determines its place value and numeric value, Represent binary numbers using combinations of decimal base 10 digits 0-9, Represent decimal numbers using combinations of binary base 2 digits 0 and 1\nKey Words: binary, number systems, bit, byte\nLesson Summary: In this lesson, students will practice representing numbers in binary (base 2). They will practice converting numbers and explore the concept of place value in the context of binary numbers.\nRelated Subjects: mathematics, engineering\n--\n\nLesson Title: Pygame Shapes\nSubject: Computer Science\nObjectives: Draw shapes on a surface display using RGB values and x,y coordinates on a cartesian plane, Explain how images are represented digitally using values of red, green, and blue, Understand how to set up a basic Pygame project framework\nKey Words: RGB, blit, surface,\nLesson Summary: In this lesson, students will create abstract art using drawn shapes in PyGame.\nRelated Subjects: art, geometry, algebra, graphic design\n--\n\nLesson Title: The Industrial Revolution\nSubject: History\nObjectives: Identify the technological advances that made the Industrial Revolution possible, Analyze the changing conditions created by the Industrial Revolution in both Europe and the United States\nKey Words: modernization, proletariat, capitalism, infrastructure\nLesson Summary: In this lesson, students make connections between the first inventions of the 19th century and the great social changes that affected slavery and imperialism.\nRelated Subjects: engineering, computer science\n--\n\nLesson Title: Learn to Program With Music\nSubject: Computer Science\nObjectives: Create digital artifacts that foster creative expression including programs, digital music, videos, images, documents, and combinations of these such as infographics, presentations, and web pages, Understand and use software tools by combining and modifying existing artifacts or by creating new artifacts\nKey Words: function, software, API, digital artifact\nLesson Summary: In this lesson, students will be introduced to programming concepts using music. Students will create artifacts with a practical, personal, or societal intent. \nRelated Subjects: music, graphic design\n--\n\nLesson Title: Simple to Complex Machines\nSubject: Robotics\nObjectives: Explore simple and compound machines and how they are used in robot manipulators, Consider the scalar and vector forces that affect how manipulators accomplish work, Design a manipulator and analyze the forces involved\nKey Words: scalar, vector, manipulator, simple machine\nLesson Summary: In this lesson, students will compare simple and compound machines in the real world. Students will develop a manipulator to accomplish a class task.\nRelated Subjects: physics, engineering\n--\n\nLesson Title: Macromolecules\nSubject: Biology\nObjectives: Understand how organisms use macromolecules to function, Identify the different types of macromolecules found in living species, Describe the relationships between the structure of macromolecules and their functions\nKey Words: biochemistry, biomolecules, macromolecules, structure-function relationship, endoplasmic reticulum, ribosome\nLesson Summary: In this lesson, students explore the structure and function of proteins, carbohydrates, lipids, and nucleic acids.\nRelated Subjects: chemistry, genetics\n--\n\nLesson Title: The Power of Plants\nSubject: Biology\nObjectives: Understand how plants use macromolecules such as proteins, carbohydrates, lipids, and nucleic acids to function, Describe the relationships between the structure of macromolecules and their functions, Explain how pollution can affect macromolecules in plants\nKey Words: macromolecules, biomolecules, carbohydrates, proteins, lipids, nucleic acids\nLesson Summary: In this lesson, students explore the structure and function of proteins, carbohydrates, lipids, and nucleic acids.\nRelated Subjects: chemistry\n--\n\nLesson Title: DNA Sequencing\nSubject: Biology\nObjectives: Understand how DNA sequencing can be used as a tool to answer questions about the inheritance of traits and mutations from a parent generation to another, Analyze and interpret DNA sequences to make inferences about gene functions, Identify and describe biologically interesting genes\nKey Words: sequencing, mutation, inheritance, gene, protein\nLesson Summary: In this lesson, students will analyze data from DNA sequencing and make inferences about gene functions and inheritance of traits.\nRelated Subjects: molecular biology\n--'

    updateModel = model + stringPrompt

    co = cohere.Client(apiKey)
    response = co.generate(
        model='xlarge',
        prompt=updateModel,
        max_tokens=300,
        temperature=0.8,
        k=0,
        p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop_sequences=["--"],
        return_likelihoods='NONE')
    finalResult = (stringPrompt + (response.generations[0].text)).split('\n')
    print(finalResult)

    return finalResult


def classify_lessons():
    response = apiKey.classify(
        model='large',
        inputs=["Students will understand how systems work."],
        examples=[Example(
            "In this lesson, students will practice representing numbers in binary (base 2). They will practice converting numbers and explore the concept of place value in the context of binary numbers.",
            "Computer Science"), Example(
            "In this lesson, students will explore the unique properties of water that are necessary to support life.",
            "Biology"), Example(
            "In this lesson, students will describe the movement of substances across the selective permeable membrane into or out of the cell to protect its internal environment.",
            "Biology"), Example(
            "In this lesson, students will be introduced to programming concepts using music. Students will create artifacts with a practical, personal, or societal intent.",
            "Computer Science"), Example(
            "In this lesson, students will correlate internal hearing with singing and pitch identification.", "Music"),
                  Example(
                      "In this lesson, students will sing a piece of music at sight based on the tonal, modal, chromatic, and atonal systems.",
                      "Music"), Example(
                "In this lesson, students will understand musical styles and genres in relation to the key social, political, economic, philosophical, and aesthetic forces that helped shape them.",
                "Music"), Example(
                "In this lesson, students make connections between the first inventions of the 19th century and the great social changes that affected slavery and imperialism.",
                "History"), Example(
                "In this lesson, students will students will analyze and demonstrate knowledge of the history, or change over time, of different regions of the world.",
                "History"), Example(
                "In this lesson, students will apply Gregor Mendel’s principles and concept of probability to predict traits by using a Punnett Square.",
                "Biology"), Example(
                "In this lesson, students will compare simple and compound machines in the real world. Students will develop a manipulator to accomplish a class task.",
                "Robotics"), Example(
                "In this lesson, students learn how the robot responds to command icons in sequence and bring together the concepts of time, speed, and distance.",
                "Robotics"), Example(
                "In this lesson, students learn about basic robot sensing and control similar to that used in advanced automated factories and warehouses.",
                "Robotics"), Example(
                "In this lesson, students will compare the different forms of energy and research various sustainable energy solutions.",
                "Environmental Science"), Example(
                "In this lesson the student will demonstrate the ability to use scientific skills necessary to identify and analyze environmental issues.",
                "Environmental Science"), Example(
                "In this lesson students will analyze and recognize the interrelationships in a good chain and a food web.",
                "Environmental Science"), Example(
                "In this lesson, students will describe the structure of an atom and distinguish between the two main types of chemical bonds.",
                "Chemistry"), Example(
                "In this lesson, students will explain the growth and populations and factors that influence them.",
                "Environmental Science"), Example(
                "In this lesson, students will analyze population changes in specific countries and learn about China\'s one child policy",
                "History"), Example(
                "In this lesson, students will use the art of communication to quickly persuade or convince their peers to change their minds on a variety of popular or unpopular opinions.",
                "Language Arts"), Example(
                "In this lesson, students will be using Internet resources the students find definitions and examples of hyperboles and paradox, and then create their own to share with peers, and identify their use in a current reading selection.",
                "Language Arts"), Example(
                "In this lesson, students will be able to explain clearly the rules on the present perfect tense of verbs as differentiated from the simple present and past tenses.",
                "Language Arts"),
                  Example("The student will be able to calculate the square footage of a given area.", "Math"), Example(
                "In this lesson, students will be able to use computation skills to add decimals for the correct sum.",
                "Math"), Example(
                "In this lesson, students will learn the proper way to calculate hourly wages including taxes, and tips, etc.",
                "Math"), Example(
                "In this lesson, students will describe heterogeneous mixtures, including suspensions and colloids.",
                "Chemistry"),
                  Example("Use the periodic table to identify trends in electronegativity and electron affinity.",
                          "Chemistry"), Example(
                "In this lesson, students will design and conduct an experiment to test the properties of substances.",
                "Chemistry"), Example(
                "Students program the robot to make decisions (artificial intelligence) in response to obstacles in the robot’s environment.",
                "Computer Science"), Example(
                "In this lesson, students will demonstrate the ability to analyze the movement of matter and energy through the biosphere.",
                "Biology"),
                  Example("In this lesson, students will differentiate between servo and non-servo control systems",
                          "Robotics"), Example(
                "In this lesson, students will differentiate the structure and function of each organ in the body systems.",
                "Biology"), Example(
                "In this lesson, students will indicate the names and functions of hardware ports and the parts of the motherboard and describe how the CPU processes data and instructions and controls the operation of all other devices.",
                "Computer Science"), Example(
                "In this lesson, students will discuss earth\'s systems and the biogeochemical cycles of water, carbon, nitrogen, and phosphorus.",
                "Biology"), Example(
                "In this lesson, students will discuss earth\'s systems and the biogeochemical cycles of water, carbon, nitrogen, and phosphorus.",
                "Environmental Science")])
    final = ('The confidence levels of the labels are: {}'.format(response.classifications))
    return final

promptMaterials = []


@app.route('/')
def index():  # put application's code here
    return render_template('index.html', title='GenerativEDU')


@app.route('/generate', methods=["GET", "POST"])
def generate():
    if request.method == "POST":
        lessonTitle_in = request.form.get("lTitle")
        if lessonTitle_in != "":
            promptMaterials.append("Lesson Title: " + lessonTitle_in)
        subject_in = request.form.get("sub")
        if subject_in != "":
            promptMaterials.append("Subject: " + subject_in)
        keyWords_in = request.form.get("kWords")
        if keyWords_in!= "":
            promptMaterials.append("Key Words: " + keyWords_in)
        lessonSummary_in = request.form.get("summ")
        if lessonSummary_in != "":
            promptMaterials.append("Lesson Summary: " + lessonSummary_in)
        objectives_in = request.form.get("objs_out")
        if objectives_in != "":
            promptMaterials.append("Objectives: " + objectives_in)
        relatedSubjects_in = request.form.get("rSubs")
        if relatedSubjects_in != "":
            promptMaterials.append("Related Subjects: " + relatedSubjects_in)
        finalResult = build_prompt(promptMaterials)
        '''
        label1 = finalResult[0]
        label2 = finalResult[1]
        label3 = finalResult[2]
        label4 = finalResult[3]
        label5 = finalResult[4]
        label6 = finalResult[5]
        '''
        return render_template("results.html", label1=finalResult)
    return render_template("AIToolTemp.html")


if __name__ == '__main__':
    app.run()
