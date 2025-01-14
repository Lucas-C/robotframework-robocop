*** Settings ***
Documentation  doc


*** Test Cases ***
Test
    [Documentation]  doc
    [Tags]  sometag
    Pass
    Keyword
    One More

Test with for loop
    FOR  ${elem}  IN  elem1  elem2  elem3
     ...  elem4
        Log  ${elem}  # this is valid comment
       Keyword
    END

Test with IF
    IF    ${condition}
        Keyword
    ELSE IF    ${condition}
          Keyword 2
    ELSE
        Keyword3
    END

Gold test
    [Documentation]  This is golden test
    ${some_value}    Perform Action    ${argument}
    ...                                ${another_argument}

    ${another_value}    Perform Another Action  # line comment
    IF    ${some_value}
        Do Stuff
    ELSE IF    ${another_value}
        ${some_value}    Do Stuff
    END


*** Keywords ***
Gold Keyword
    [Documentation]  This is golden test
    [Arguments]    ${arg}
    Keyword
    #  This is comment
    ${some_value}    Perform Action    ${argument}
    ...                                ${another_argument}

    ${another_value}    Perform Another Action
    IF    ${some_value}
        Do Stuff
    ELSE IF    ${another_value}
        ${some_value}    Do Stuff
    END

Keyword With Over Indented Line
    [Documentation]  this is doc
       No Operation
    #  It is also valid indent
    Pass
    No Operation
    Fail

Keyword With Under Indented Line
    [Documentation]  this is doc
    No Operation
   Pass
    No Operation
    Fail

Keyword With Over Indented Setting
    [Documentation]  this is doc
     [Arguments]  ${arg}
       No Operation
    Pass
    No Operation
    Fail

Templated Test
    [Documentation]  doc
    [Template]  Some Template
                Over Indent
                ...  Same Here
    What Goes
     [Teardown]  Over Indented

Keyword With Multiline For Loop
    [Documentation]  Keyword doc
    [Tags]  tag
    FOR  ${elem}  IN  elem1  elem2  elem3
     ...  elem4
        Log  ${elem}  # this is valid comment
       Keyword

    END

Keyword With If Block
    IF    ${condition}
        Keyword
    ELSE IF    ${condition}
        Keyword 2
    ELSE
        Keyword3
    END
    Keyword

Keyword With Under Indented For Loop Body
    FOR  ${elem}  IN  ${list}
   Log  stuff
       Keyword
       Keyword
    END

Keyword With Uneven NewLines
    [Arguments]    ${arg}
   ...    ${arg2}
    Keyword 1
    Keyword
      ...  ${2}

Keyword With Assignments
    ${arg}    ${arg}    Keyword
    ...  multiline
    IF    ${condition}
        ${value}    Correct Indent
          ${arg}  Incorrect Indent
    ELSE IF  ${flag}
         Incorrect Indent
        Correct Indent
    ELSE
        Correct Indent
    END

Keyword With Under Indented For Loop Body
    FOR  ${elem}  IN  ${list}
   Log  stuff
    END

Keyword With Multiline Keywords
    [Argument]  ${arg}
    ${return_value}    Keyword
    Keyword
    Keyword2
    Keyword
    ...    ${arg}
    ...    ${arg}
    ...    3

Keyword With Tabulators
    Keyword Without Tab
	Keyword  1
	Keyword  2
	Keyword  3  3
	Keyword  4
