# import json
# import yaml
import os
from termcolor import colored
from models.openai_models import get_open_ai, get_open_ai_json, get_open_ai_audio, get_open_ai_with_structured_output
from prompts.prompts import (
    cleaner_prompt_template,
    functional_requirements_definer_prompt_template,
    budgeter_prompt_template,
)
from utils.helper_functions import check_for_content, create_excel_from_budget
from states.state import AgentGraphState
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from typing import List
from pydantic import BaseModel, Field, ValidationError

from pydub import AudioSegment

class Agent:
    def __init__(self, state: AgentGraphState, model=None, server=None, temperature=0):
        self.state = state
        self.model = model
        self.server = server
        self.temperature = temperature

    def get_llm(self, json_model=True, audio_model=False, structured_output_model=False, pydantic_model=None):
        if self.server == 'openai':
            if structured_output_model:
                return get_open_ai_with_structured_output(model=self.model, temperature=self.temperature, pydantic_model=pydantic_model)
            else:
                return get_open_ai_audio() if audio_model else get_open_ai_json(model=self.model, temperature=self.temperature) if json_model else get_open_ai(model=self.model, temperature=self.temperature)

    def update_state(self, key, value):
        self.state = {**self.state, key: value}

class TranscriberAgent(Agent):
    def invoke(self, user_input):

        READ_FROM_FILE = True

        if READ_FROM_FILE:
            # leemos el archivo audio_transcription.txt y lo guardamos su contenido en la variable transcription
            with open("./llm_outputs/audio_transcription.txt", "r") as file:
                full_transcription = file.read()

        else:
            llm = self.get_llm(audio_model=True)
            # Verificamos la ruta absoluta
            file_path = "./audio_files/Carlos.mp3"

            # Verificamos si el archivo existe en la ruta especificada
            if not os.path.exists(file_path):
                print("El archivo no existe en la ruta especificada.")
            else:
                # Intentamos cargar el archivo
                try:
                    song = AudioSegment.from_mp3(file_path)
                    print("Archivo cargado correctamente.")
                except Exception as e:
                    print("Error al cargar el archivo:", e)

                # Definimos el tamaño máximo del archivo en bytes (24MB)
                max_size_bytes = 24 * 1024 * 1024
                chunk_size_ms = len(song) * (max_size_bytes / os.path.getsize(file_path))  # Calculamos el tamaño del chunk en milisegundos

                transcriptions = []  # Lista para almacenar todas las transcripciones

                # Dividimos el archivo en trozos de 24 MB
                for i in range(0, len(song), int(chunk_size_ms)):
                    print("iteracion: ", i)
                    chunk = song[i:i + int(chunk_size_ms)]
                    chunk_file_path = f"./audio_files/Carlos_chunk_{i}.mp3"
                    chunk.export(chunk_file_path, format="mp3")
                    
                    # Abrimos el archivo de chunk
                    with open(chunk_file_path, "rb") as audio_file:
                        transcription = llm.audio.transcriptions.create(
                            model="whisper-1", 
                            file=audio_file,
                            language="es",
                            response_format="text",
                        )
                        transcriptions.append(transcription)
                    
                    # Eliminamos el archivo de chunk después de procesarlo si ya no es necesario
                    os.remove(chunk_file_path)

                # Unificamos todas las transcripciones en una sola variable
                full_transcription = " ".join(transcriptions)


        self.update_state("audio_transcription", full_transcription)
        print(colored(f"transcriber 👩🏿‍💻: {full_transcription}", 'cyan'))
        return self.state

class CleanerAgent(Agent):
    def invoke(self, user_input, audio_transcription, prompt=cleaner_prompt_template, feedback=None):
        READ_FROM_FILE = True

        if READ_FROM_FILE:
            with open("./llm_outputs/cleaned_audio_transcription.txt", "r") as file:
                cleaned_transcription = file.read()
        else:
            audio_transcription = audio_transcription() if callable(audio_transcription) else audio_transcription
            
            cleaner_prompt = prompt.format(
                audio_transcription=audio_transcription,
            )
            messages = [
                SystemMessage(content=cleaner_prompt)
            ]

            llm = self.get_llm(json_model=False)
            ai_msg = llm.invoke(messages)
            cleaned_transcription = check_for_content(ai_msg)

        print(colored(f"Cleaner 🧑🏼‍💻: {cleaned_transcription}", 'green'))
        self.update_state("cleaned_audio_transcription", cleaned_transcription)
        
        return self.state
    
class FunctionalRequirementsDefinerAgent(Agent):
    def invoke(self, user_input, cleaned_audio_transcription, prompt=functional_requirements_definer_prompt_template, feedback=None):

        READ_FROM_FILE = True

        if READ_FROM_FILE:
            with open("./llm_outputs/functional_requirements.txt", "r") as file:
                functional_requirements = file.read()
        else:
            cleaned_audio_transcription = cleaned_audio_transcription() if callable(cleaned_audio_transcription) else cleaned_audio_transcription
            
            functional_requirements_definer_prompt = prompt.format(
                cleaned_audio_transcription=cleaned_audio_transcription,
            )
            messages = [
                SystemMessage(content=functional_requirements_definer_prompt)
            ]

            llm = self.get_llm(json_model=False)
            ai_msg = llm.invoke(messages)
            functional_requirements = check_for_content(ai_msg)

        print(colored(f"Functional Requirements Definer 🧑🏼‍💻: {functional_requirements}", 'yellow'))
        self.update_state("functional_requirements", functional_requirements)
        
        return self.state
    
class BudgeterAgent(Agent):
    def invoke(self, user_input, functional_requirements, prompt=budgeter_prompt_template, feedback=None):
        functional_requirements = functional_requirements() if callable(functional_requirements) else functional_requirements

        
        budgeter_prompt = prompt.format(
            functional_requirements=functional_requirements,
        )
        messages = [
            SystemMessage(content=budgeter_prompt)
        ]

        class Gasto(BaseModel):
            area: str = Field(..., description="El área a la que pertenece el gasto.")
            nombre: str = Field(..., description="El nombre del gasto.")
            descripcion: str = Field(..., description="Una descripción del gasto.")
            horas: int = Field(..., description="La cantidad de horas que se gastarán.")
            costo: int = Field(..., description="La cantidad de dinero que se gastará teniendo en cuenta que el precio por hora es de 60 euros.")
        class Presupuesto(BaseModel):
            resumen: str = Field(..., description="Un resumen del presupuesto.")
            gastos: List[Gasto] = Field(..., description="Una lista de los gastos.")
            total_horas: int = Field(..., description="El total de horas presupuestadas.")
            total_costo: int = Field(..., description="El total de costo presupuestado teniendo en cuenta que el precio por hora es de 60 euros.")
            total_costo_con_margen_adicional: int = Field(..., description="El total de costo presupuestado con un margen adicional del 15% para posibles imprevistos.")
            consideraciones: str = Field(..., description="Consideraciones adicionales del presupuesto.")

        

        llm = self.get_llm(structured_output_model=True, pydantic_model=Presupuesto)
        ai_msg = llm.invoke(messages)
        budget = check_for_content(ai_msg)

        print(colored(f"Budgeter 🧑🏼‍💻: {budget}", 'magenta'))
        create_excel_from_budget(budget)
        self.update_state("budget", budget)
        
        return self.state
    


class EndNodeAgent(Agent):
    def invoke(self):
        self.update_state("end_chain", "end_chain")
        return self.state