import sounddevice as sd

print("Host APIs:")
for i, api in enumerate(sd.query_hostapis()):
    print(f"  [{i}] {api['name']}")

print()
default_api = sd.query_hostapis(sd.default.hostapi)
print(f"Default API: {default_api['name']}")
print(f"Default device: {sd.default.device}")

# Try different APIs
devices = sd.query_devices()
for api_idx in range(len(sd.query_hostapis())):
    api_devices = [d for d in devices if d["hostapi"] == api_idx and d["max_input_channels"] > 0]
    if api_devices:
        api_name = sd.query_hostapis(api_idx)["name"]
        for d in api_devices:
            print(f"  API {api_idx} ({api_name}) - Dev [{d['index']}] {d['name']} @ {d['default_samplerate']}Hz")
