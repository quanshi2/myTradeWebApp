# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 22:03:34 2022

@author: Yun An Shi
"""

import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

# Create a table
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

# draw chart
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

# Widgets， slider
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

