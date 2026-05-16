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

#Memory table parsing

Bottom_button = driver.find_element(by=By.CSS_SELECTOR,value=".button-dmem-bottom")
Top_button = driver.find_element(by=By.CSS_SELECTOR,value=".button-dmem-top")
Up_button = driver.find_element(by=By.CSS_SELECTOR,value=".button-dmem-up")
Down_button = driver.find_element(by=By.CSS_SELECTOR,value=".button-dmem-down")
Ascii_button = driver.find_element(by=By.ID, value = "button-ascii")


Mem_table_rows = len(driver.find_elements(By.XPATH,"/html/body/div[1]/div[4]/div[2]/div[2]/div[2]/table/tbody/tr"))
Mem_table_cols = len(driver.find_elements(By.XPATH,"/html/body/div[1]/div[4]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td"))

print(Mem_table_rows)
print(Mem_table_cols)



program_box.clear()
file = open('INSTRUCTION_TESTV2.S','r') 
program_text = file.read()
file.seek(0,0)
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


time.sleep(1)
INSTRUCTIONS_THAT_INTERACT_WITH_MEMORY = ["LD ","ST ","STD ","STS ","LDD ","PUSH ","POP "]

with Progress() as p:
    t = p.add_task("Executing step by step...",total= 826)
    last_pc = 0
    print("hello")
    instructions_executed = 0 
    loop = True
    while loop:
        intermediary_list = []
        REGISTER_VALUES_THIS_ITERATION = []
        mem_address_vals = {}
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

        #print(REGISTER_VALUES_THIS_ITERATION)
        intermediary_list.append(REGISTER_VALUES_THIS_ITERATION)

        instruction = driver.find_element(By.ID,"pmem-line-{val}".format(val = (instructions_executed%8))) #this value is not representative of the instruction executed any more
        #print(lines_instruction)
        instruction = instruction.text
        #print(instruction)
        intermediary_list.append(instruction)
        test = -1
        for item in INSTRUCTIONS_THAT_INTERACT_WITH_MEMORY:
            test = instruction.find(item)
            if test != -1:
                break 
        
        if test != -1:
            Top_button.click()
            #Optaning data from memory
            for tables in range(32):
                for r in range(1,Mem_table_rows+1):
                    row = driver.find_element(By.XPATH,"/html/body/div[1]/div[4]/div[2]/div[2]/div[2]/table/tbody/tr["+str(r)+"]").text
                    elements = row.split("\n")
                    address_start = int(elements[0])
                    for g in range(1,Mem_table_cols+1):
                        #value = driver.find_element(By.XPATH,"/html/body/div[1]/div[4]/div[2]/div[2]/div[2]/table/tbody/tr["+str(r)+"]/td["+str(p)+"]").text
                        value = int(elements[g])
                        if value != 0:
                            mem_address_vals[address_start+g] = value
                Down_button.click()
  

        intermediary_list.append(mem_address_vals)
        INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES.append(intermediary_list)
        #print(INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instructions_executed])
        instructions_executed += 1

        p.update(t,advance=1)
        #print(lines_instruction.text)
        if last_pc == int(PC.text):
            loop = False
        else: 
            last_pc = int(PC.text)
#Writing INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES to file 
with open('EXPECTED_REGISTER_VALUESV2.txt','w+') as f:

    for items in INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES:
        f.write('%s\n' %items)
    print("File written successfully")

f.close()

driver.quit()
End_Time =  time.time()
print("The opperation took:",End_Time-start_time)
