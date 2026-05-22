import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="Python Multi-Graph Math Tool", layout="wide")

if 'functions' not in st.session_state:
    st.session_state.functions = []

st.sidebar.title("수식 관리자")

with st.sidebar.expander("새 수식 추가", expanded=True):
    new_formula = st.text_input("f(x) =", "sin(x) * x")
    color_options = ["Red", "Blue", "Green", "Black", "Orange", "Purple", "DeepPink", "Brown", "Gold"]
    new_color = st.selectbox("그래프 색상", color_options)
    
    if st.button("목록에 추가"):
        try:
            test_formula = new_formula.replace('^', '**').lower()
            transformations = standard_transformations + (implicit_multiplication_application,)
            expr = parse_expr(test_formula, transformations=transformations, local_dict={'e': sp.E, 'pi': sp.pi})
            
            if any(s.name != 'x' for s in expr.free_symbols):
                st.error("변수는 'x'만 사용할 수 있습니다.")
            else:
                st.session_state.functions.append({
                    'formula': new_formula,
                    'color': new_color.lower(),
                    'visible': True
                })
                st.rerun()
        except Exception as e:
            st.error(f"해석 불가: {e}")

with st.sidebar.expander("입력 가이드"):
    st.markdown("""
    - **사칙연산**: `+`, `-`, `*`, `/`
    - **제곱/루트**: `x**2` (또는 `x^2`), `sqrt(x)`
    - **삼각함수**: `sin`, `cos`, `tan`
    - **상수**: `pi`, `E`
    """)

st.sidebar.markdown("---")
st.sidebar.subheader("그래프 목록")
for i, func in enumerate(st.session_state.functions):
    cols = st.sidebar.columns([0.1, 0.7, 0.2])
    func['visible'] = cols[0].checkbox("", value=func['visible'], key=f"check_{i}")
    cols[1].markdown(f"<span style='color:{func['color']}'>`{func['formula']}`</span>", unsafe_allow_html=True)
    if cols[2].button("✕", key=f"del_{i}"):
        st.session_state.functions.pop(i)
        st.rerun()

st.title("Python Multi-Graph Math Tool")
st.caption("SymPy와 Matplotlib을 활용한 실시간 그래프 시각화 도구")

fig, ax = plt.subplots(figsize=(10, 6))

ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.grid(True, which='both', linestyle='-', linewidth=0.5, color='#e0e0e0')
ax.minorticks_on()
ax.set_facecolor('white')

x_vals = np.linspace(-15, 15, 2000)
x_sym = sp.symbols('x')
any_plotted = False

for func in st.session_state.functions:
    if func['visible']:
        try:
            formula_str = func['formula'].replace('^', '**').lower()
            transformations = standard_transformations + (implicit_multiplication_application,)
            expr = parse_expr(formula_str, transformations=transformations, local_dict={'e': sp.E, 'pi': sp.pi})
            
            f_lamb = sp.lambdify(x_sym, expr, "numpy")
            y_vals = f_lamb(x_vals)
            
            if not isinstance(y_vals, np.ndarray):
                y_vals = np.full_like(x_vals, y_vals, dtype=float)
            
            dy = np.abs(np.diff(y_vals, prepend=y_vals[0]))
            y_vals[dy > 50] = np.nan 
            
            ax.plot(x_vals, y_vals, color=func['color'], lw=2.5, label=func['formula'])
            any_plotted = True
        except:
            continue

ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])

if any_plotted:
    ax.legend(loc='upper right', frameon=True, shadow=True)


st.pyplot(fig)