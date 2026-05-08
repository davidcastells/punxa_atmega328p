import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 
from rich.progress import Progress
import time



start_time = time.time()

driver = webdriver.Chrome()

url ='https://jonopriestley.github.io/avrsim/'
driver.get(url)

print(driver.title)


#regTable =  driver.find_element(By.CLASS_NAME,"table table-reg")
program_box = driver.find_element(by=By.NAME, value="code_box")

Compile_button = driver.find_element(by=By.CSS_SELECTOR, value=".button-assemble")
Step_button = driver.find_element(by=By.CSS_SELECTOR, value=".button-step")
Base_button = driver.find_element(by=By.ID, value="button_base")

program_box.clear()
file = open('INSTRUTION_TEST.S','r') 
program_text = file.read()
file.seek(0,0)
Steps = len(file.readlines())
Steps -= 6
print(Steps)
pyperclip.copy(program_text)

program_box.send_keys(Keys.CONTROL,'v') #copy paste the code

file.close()
Base_button.click()
Compile_button.click()
#getting the execution information for each instruction
INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES = [#{R0 to R31} {STREG} {PROGRAM COUNTER} {STACK POINTER} {Memory Change} if address:0 and val:0 the memory test is skiped 
    #R:0|R:1|R:2|R:3|R:4|R:5|R:6|R:7|R:8|R:9|R:10|R:11|R:12|R:13|R:14|R:15|R:16|R:17|R:18|R:19|R:20|R:21|R:22|R:23|R:24|R:25|R:26|R:27|R:28|R:29|R:30|R:31|SREG      |PC|SP  |Memory Change
#    [0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0    ,0  ,0b00000000,0,0],

]


with Progress() as p:
    t = p.add_task("Executing step by step...", total=Steps)
    loop = True
    while loop:
        REGISTER_VALUES_THIS_ITERATION = []
        Step_button.click()

        for i in range(31):
            reg = driver.find_element("id","reg-{}".format(i))
            REGISTER_VALUES_THIS_ITERATION.append(reg.text)

        I = driver.find_element("id","sreg-I")
        T = driver.find_element("id","sreg-T")
        H = driver.find_element("id","sreg-H")
        S = driver.find_element("id","sreg-S")
        V = driver.find_element("id","sreg-V")
        N = driver.find_element("id","sreg-N")
        Z = driver.find_element("id","sreg-Z")
        C = driver.find_element("id","sreg-C")

        SREG = I.text + T.text + H.text + S.text + V.text + N.text + Z.text + C.text
        #print(SREG)
        SREG = int(SREG,2)
        REGISTER_VALUES_THIS_ITERATION.append(SREG)

        PC = driver.find_element("id","reg-PC")
        SP = driver.find_element("id","reg-SP")
        X = driver.find_element("id","reg-X")
        Y = driver.find_element("id","reg-Y")
        Z = driver.find_element("id","reg-Z")

        REGISTER_VALUES_THIS_ITERATION.append(PC.text)
        REGISTER_VALUES_THIS_ITERATION.append(SP.text)
        #REGISTER_VALUES_THIS_ITERATION.append(X.text)
        #REGISTER_VALUES_THIS_ITERATION.append(Y.text)
        #REGISTER_VALUES_THIS_ITERATION.append(Z.text)

        #I don't take in to account the writing to memory operations

        print(REGISTER_VALUES_THIS_ITERATION)
        INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES.append(REGISTER_VALUES_THIS_ITERATION)

        lines_instruction = driver.find_element("id","pmem-line-{}".format(i%8))

        #INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES.append(lines_instruction.text)
        p.update(t,advance=1)
        #print(lines_instruction.text)
        if lines_instruction.text == 'NOP':
            loop = False

#Writing INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES to file 
with open('EXPECTED_REGISTER_VALUES.txt','w+') as f:

    for items in INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES:
        f.write('%s\n' %items)
    print("File written successfully")

f.close()

driver.quit()
End_Time =  time.time()
print("The opperation took:",End_Time-start_time)
