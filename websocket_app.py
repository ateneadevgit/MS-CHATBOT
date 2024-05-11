import json
import asyncio
import websockets

responses_file_path = "assets/responses.json"

with open(responses_file_path, 'r', encoding='utf-8') as file:
    responses_dict = json.load(file)

async def chatbot_handler(websocket, path):
    print(f"Connection established from {websocket.remote_address}")

    try:
        message_id = 0
        outer_option = 0
        inner_option = 0

        outer_options_ls = [el + ". " + responses_dict[el]["title"] for el in responses_dict.keys() if "title" in responses_dict[el].keys()]

        while True:

            try: 
                # Very first message
                if message_id == 0:
                    greeting = responses_dict["greeting"]["text"]
                    await websocket.send(greeting)
                    await websocket.send("\n".join(outer_options_ls))
                    message_id += 2

                # Has not picked outer option
                elif outer_option == 0:
                    received_outer_option = await websocket.recv()
                    print(f"Received outer option: {received_outer_option}")
                    inner_options = [el + ". " + responses_dict[received_outer_option]["options"][el]["title"] for el in responses_dict[received_outer_option]["options"]] 
                    outer_option = received_outer_option
                    await websocket.send("\n".join(inner_options))
                    message_id += 1
                    
                # Has already picked outer option
                elif outer_option != 0:
                    received_inner_option = await websocket.recv()
                    print(f"Received inner option: {received_inner_option}")
                    if received_inner_option == "Volver" and inner_option == 0:
                        print("Back outer")
                        await websocket.send("\n".join(outer_options_ls))
                        message_id += 1
                        outer_option = 0
                    elif received_inner_option == "Volver" and inner_option != 0:
                        print("Back inner")
                        inner_options = [el + ". " + responses_dict[received_outer_option]["options"][el]["title"] for el in responses_dict[received_outer_option]["options"]] 
                        outer_option = received_outer_option
                        await websocket.send("\n".join(inner_options))
                        message_id += 1
                        inner_option = 0
                    else:
                        inner_option_response = responses_dict[received_outer_option]["options"][received_inner_option]["response"]
                        inner_option = received_inner_option
                        await websocket.send(inner_option_response)
                        message_id += 1
            except Exception as e:
                print("Exception => ", str(e))
                await websocket.send("Opción inválida")
    except websockets.ConnectionClosed:
        print("Connection closed")

# Start the WebSocket server
start_server = websockets.serve(chatbot_handler, "0.0.0.0", 8013)

# Run the server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
