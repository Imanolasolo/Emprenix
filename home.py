import streamlit as st

def home_show():

    col1,col2= st.columns(2)
    with col1:
        st.subheader('We are committed to your grow!')
        st.text('Do you want to grow as professional or company with AI solutions?')
        st.text('Are you tired on making the same things getting the same results?')
        st.text('Do you want to be the very owner of your business or project?')
    with col2:
        st.warning('You reached to the right place')
        with st.expander("What can we do for you?"):
            st.write('''
            1- Creation of electronic personality.
                     
            2- Improve your social presence.
                     
            3- Grow your business with AI powered tools.
                     
            4- Walk with you in every step of AI journey to the success of your project!         
            ''')


