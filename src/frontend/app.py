import streamlit as st
from research_crew.crew import ResearchCrew


class ResearchCrewUI:

    def load_html_template(self):
        with open("src/research_crew/config/research_template.html", "r") as file:
            html_template = file.read()

        return html_template

    def generate_research(self, topic):
        inputs = {
            "topic": topic,
            "html_template": self.load_html_template(),
        }
        return ResearchCrew().crew().kickoff(inputs=inputs)

    def research_generation(self):

        if st.session_state.generating:
            st.session_state.research = self.generate_research(
                st.session_state.topic
            )

        if st.session_state.research and st.session_state.research != "":
            with st.container():
                st.write("Research generated successfully!")
                st.download_button(
                    label="Download HTML file",
                    data=st.session_state.research,
                    file_name="research.html",
                    mime="text/html",
                )
            st.session_state.generating = False

    def sidebar(self):
        with st.sidebar:
            st.title("Research Crew")

            st.write(
                """
                To conduct research on a topic, enter a topic. \n
                Your team of AI agents will generate research report for you!
                """
            )

            st.text_input("Topic", key="topic", placeholder="Koalas")

            if st.button("Generate Report"):
                st.session_state.generating = True

    def render(self):
        st.set_page_config(page_title="Research Crew", page_icon="🐨")

        if "topic" not in st.session_state:
            st.session_state.topic = ""

        if "research" not in st.session_state:
            st.session_state.research = ""

        if "generating" not in st.session_state:
            st.session_state.generating = False

        self.sidebar()

        self.research_generation()


if __name__ == "__main__":
    ResearchCrewUI().render()

