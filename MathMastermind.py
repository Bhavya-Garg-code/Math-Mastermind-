from openai import OpenAI
import time
import streamlit as  st
api = st.secrets['API']
client = OpenAI(api_key = api,base_url = 
"https://api.groq.com/openai/v1")
model = 'openai/gpt-oss-20b'

sys_pro = """
You are a math mastermind.
You have to behave like a maths teacher.
Explain every solution properly with logical reasoning and clarity
IMPORTANT FORMATTING RULES:

1. Use plain text for mathematical equations.

2. Do NOT use LaTeX syntax.

3. Do NOT use dollar signs for equations.

4. Do NOT use \\( \\), \\[ \\], \\frac, \\boxed, or other LaTeX commands.

5. Write x² instead of x^2 where appropriate.

6. Write fractions as 1/2, square roots as sqrt(25) = 5,

and multiplication using ×.

7. Use clear headings and numbered steps.

8. Put each equation on a separate line.

9. End with a clearly labelled FINAL ANSWER.

10. Verify the answer when possible.

Use this format:

PROBLEM:

Write the given problem.

STEP 1: ...

Explanation...

STEP 2: ...

Explanation...

FINAL ANSWER:

Write the final answer clearly.

VERIFICATION:

Check the answer if possible.
"""

def solve(problem,level):
    prompt = f"""
{sys_pro}
level:{level}
problem:{problem}
"""
    try:
      response = client.chat.completions.create(
        model = model,
        messages = [
           {'role':'system', 'content':sys_pro},
           {'role':'user','content':prompt}],
        temperature=0.3,
        max_tokens = 2056
    )
      return response.choices[0].message.content
    except Exception as e:
       return f'Error Occured : {e}'

st.set_page_config('Math Mastermind', layout = 'wide')
st.title("Math Mastermind")

st.write("Enter a problem to get easy solutions")
if('history' not  in st.session_state):
   st.session_state.history = []

problem = st.text_area("math problem", placeholder = ' x+y = 5')
level = st.selectbox('level',['Basic','moderate','Advanced'])

if(st.button('solve')):
   if not problem.strip():
      st.warning("Please enter a problem")
   else:
      with st.spinner("Solving"):
         try:
            ans = solve(problem,level)
            st.session_state.history.append({
               'Problem':problem,
               'Answer':ans
            }
            )
            st.subheader("Solution")
            st.markdown(ans)

         except Exception as e:
            st.warning(f"Error Occured {e}")
if st.session_state.history:
   st.divider()
   st.subheader('Solutiion history')

   for i,item in enumerate(reversed(st.session_state.history),1):
      with st.expander(f"Q{i}: {item['Problem']}"):
         st.markdown(item['Answer'])
         
if(st.button('Clear history')):
   st.session_state.history = []
   st.rerun()
