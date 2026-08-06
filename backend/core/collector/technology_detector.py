import json


class TechnologyDetector:

    def detect(self, repository):

        repository.technology_stack.clear()

        package_json = repository.config_files.get("package.json")

        if package_json:

            try:
                with open(package_json, "r", encoding="utf-8") as file:

                    data = json.load(file)

                    dependencies = {}

                    dependencies.update(data.get("dependencies", {}))
                    dependencies.update(data.get("devDependencies", {}))

                    self._detect_node(dependencies, repository)

            except Exception:
                pass

        requirements = repository.config_files.get("requirements.txt")

        if requirements:

            try:
                with open(requirements, "r", encoding="utf-8") as file:

                    packages = file.read().lower()

                    self._detect_python(packages, repository)

            except Exception:
                pass

        return repository

    def _add(self, repository, category, technology):

        if category not in repository.technology_stack:
            repository.technology_stack[category] = []

        if technology not in repository.technology_stack[category]:
            repository.technology_stack[category].append(technology)

    def _detect_node(self, dependencies, repository):

        mapping = {
            "next": ("Frontend", "Next.js"),
            "react": ("Frontend", "React"),
            "vue": ("Frontend", "Vue.js"),
            "@angular/core": ("Frontend", "Angular"),

            "tailwindcss": ("Styling", "Tailwind CSS"),
            "bootstrap": ("Styling", "Bootstrap"),
            "@mui/material": ("Styling", "Material UI"),

            "express": ("Backend", "Express.js"),

            "axios": ("Utilities", "Axios"),

            "firebase": ("Database", "Firebase"),
            "@supabase/supabase-js": ("Database", "Supabase"),
            "mongoose": ("Database", "MongoDB"),
            "prisma": ("Database", "Prisma"),

            "redux": ("State Management", "Redux"),
            "zustand": ("State Management", "Zustand"),

            "openai": ("AI / ML", "OpenAI"),
            "@google/generative-ai": ("AI / ML", "Gemini"),
            "langchain": ("AI / ML", "LangChain"),
        }

        for package in dependencies:

            if package in mapping:

                category, technology = mapping[package]

                self._add(repository, category, technology)

    def _detect_python(self, packages, repository):

        mapping = {
            "flask": ("Backend", "Flask"),
            "django": ("Backend", "Django"),
            "fastapi": ("Backend", "FastAPI"),
            "streamlit": ("Backend", "Streamlit"),

            "tensorflow": ("AI / ML", "TensorFlow"),
            "torch": ("AI / ML", "PyTorch"),
            "scikit-learn": ("AI / ML", "Scikit-Learn"),
            "numpy": ("AI / ML", "NumPy"),
            "pandas": ("AI / ML", "Pandas"),
            "langchain": ("AI / ML", "LangChain"),
            "google-generativeai": ("AI / ML", "Gemini"),
        }

        for package, (category, technology) in mapping.items():

            if package in packages:
                self._add(repository, category, technology)