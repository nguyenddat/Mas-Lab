async def get_chat_completion(llm, prompt, parser, params):
    chain = prompt | llm | parser
    response = await chain.ainvoke(params)

    if not isinstance(response, list) and not isinstance(response, dict):
        response = response.dict()  
    
    return response