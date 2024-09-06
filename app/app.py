from agent_graph.graph import create_graph, compile_workflow

server = 'openai'
model = 'gpt-4o-mini'

iterations = 40

print ("Creando el grafo de LangGraph")
graph = create_graph(server=server, model=model)
workflow = compile_workflow(graph)
print ("Grafo creado.")

if __name__ == "__main__":

    verbose = False
    dict_inputs = {"user_input": 'test'}
    limit = {"recursion_limit": iterations}


    for event in workflow.stream(
        dict_inputs, limit
        ):
        if verbose:
            print("\nState actual:", event)
        else:
            print("\n")




    