import streamlit as st
from extract_resume import extract_text_from_bytes
from analyze import analyze, rewrite_resume

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")
st.title("📄 AI Resume Analyzer")
st.caption("अपना resume और job description दो, और match score व सुझाव पाओ।")

uploaded = st.file_uploader("Resume upload करो (PDF)", type=["pdf"])
jd_text = st.text_area("Job Description यहाँ paste करो", height=250)
want_rewrite = st.checkbox("Resume को JD के हिसाब से rewrite भी करो")

if st.button("Analyze करो", type="primary"):
    if not uploaded or not jd_text.strip():
        st.warning("पहले resume upload करो और JD paste करो।")
        st.stop()

    with st.spinner("Analysis हो रहा है..."):
        try:
            resume_text = extract_text_from_bytes(uploaded.read())
            if not resume_text:
                st.error("Resume से text नहीं निकला। शायद PDF scanned (image) है।")
                st.stop()
            result = analyze(resume_text, jd_text)
        except Exception as e:
            st.error(f"Analysis में गड़बड़ हुई: {e}")
            st.stop()

    score = result["match_score"]
    col1, col2 = st.columns(2)
    col1.metric("Match Score", f"{score}%")
    col2.metric("Experience Level", result["experience_level"])
    st.progress(min(max(score, 0), 100) / 100)

    st.subheader("Summary")
    st.write(result["summary"])

    st.subheader("✅ Strengths")
    for s in result["strengths"]:
        st.markdown(f"- {s}")

    st.subheader("⚠️ Missing Skills")
    for m in result["missing_skills"]:
        st.markdown(f"- {m}")

    st.subheader("💡 Suggestions")
    for s in result["suggestions"]:
        st.markdown(f"- {s}")

    if want_rewrite:
        with st.spinner("Resume rewrite हो रहा है..."):
            try:
                rewritten = rewrite_resume(resume_text, jd_text)
            except Exception as e:
                st.error(f"Rewrite में गड़बड़ हुई: {e}")
                st.stop()
        st.subheader("✍️ JD के हिसाब से Rewritten Resume")
        st.markdown(rewritten)
        st.download_button(
            "Download करो (.txt)",
            rewritten,
            file_name="tailored_resume.txt",
        )