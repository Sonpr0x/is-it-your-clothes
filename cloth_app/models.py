def Upload_person():
    client = Client("zhengchong/CatVTON")
    result = client.predict(
		image_path=handle_file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),
		api_name="/person_example_fn"
)
    return result

def Upload_cloth():
    #return local filepath

def Process():
    result = client.predict(
		person_image={"background":handle_file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),"layers":[],"composite":None},
		cloth_image=handle_file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),
		cloth_type="upper",
		num_inference_steps=50,
		guidance_scale=2.5,
		seed=42,
		show_type="input & mask & result",
		api_name="/submit_function"
    )

    return result
