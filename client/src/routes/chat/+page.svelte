<script lang="ts">
	interface Message {
		text: string;
		isSent: boolean;
		image: string | null;
	}

	let msg = $state('');
	let messages: Message[] = $state([
		{ text: 'Hey there! 👋', isSent: false, image: null },
		{ text: 'Hi! How are you?', isSent: true, image: null },
		{ text: "I'm doing great, thanks for asking!", isSent: false, image: null }
	]);
	let isStreaming = $state(false);
	let currentStreamingMessage = $state('');
	let selectedImage: File | null = $state(null);
	let imagePreview: string | null = $state(null);

	async function sendMessage() {
		if (!msg.trim() && !selectedImage) return;
		if (isStreaming) return;

		// Add user message to chat
		const userMessage = { text: msg, isSent: true, image: imagePreview };
		msg = '';
		messages = [...messages, userMessage];

		// Clear the selected image and preview after adding to messages
		selectedImage = null;
		imagePreview = null;

		isStreaming = true;
		currentStreamingMessage = '';

		try {
			// Send the text message to the existing endpoint
			const response = await fetch('http://localhost:8000/ollama/generate', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ prompt: userMessage.text })
			});

			const reader = response.body?.getReader();
			if (!reader) throw new Error('No reader available');

			while (true) {
				const { done, value } = await reader.read();
				if (done) break;

				// Convert the chunk to text and append it
				const chunk = new TextDecoder().decode(value);
				currentStreamingMessage = chunk;
			}

			// Add the complete response to messages
			messages = [...messages, { text: currentStreamingMessage, isSent: false, image: null }];
			currentStreamingMessage = '';
		} catch (error) {
			console.error('Error:', error);
			messages = [
				...messages,
				{ text: 'Sorry, there was an error processing your message.', isSent: false, image: null }
			];
		} finally {
			isStreaming = false;
		}
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			sendMessage();
		}
	}

	function handleImageChange(event: Event) {
		const target = event.target as HTMLInputElement;
		selectedImage = target.files ? target.files[0] : null;

		if (selectedImage) {
			const reader = new FileReader();
			reader.onload = () => {
				imagePreview = reader.result as string;
			};
			reader.readAsDataURL(selectedImage);
		} else {
			imagePreview = null;
		}
	}
</script>

<div class="flex h-screen flex-col bg-gray-100">
	<!-- Chat container -->
	<div class="flex-1 overflow-y-auto p-4">
		<div class="mx-auto max-w-3xl space-y-4">
			{#each messages as message}
				<div class="flex {message.isSent ? 'justify-end' : 'justify-start'}">
					<div
						class="{message.isSent
							? 'rounded-l-lg rounded-tr-lg bg-blue-500 text-white'
							: 'rounded-r-lg rounded-tl-lg bg-white text-gray-800'} 
            max-w-[70%] p-3 shadow-sm"
					>
						{#if message.image}
							<img src={message.image} alt="Uploaded" class="max-w-full rounded-lg" />
						{/if}
						{message.text}
					</div>
				</div>
			{/each}
			{#if isStreaming}
				<div class="flex justify-start">
					<div class="max-w-[70%] rounded-r-lg rounded-tl-lg bg-white p-3 text-gray-800 shadow-sm">
						{currentStreamingMessage}
						<span class="animate-pulse">▋</span>
					</div>
				</div>
			{/if}
		</div>
	</div>

	<!-- Image preview -->
	{#if imagePreview}
		<div class="mx-auto max-w-3xl p-4">
			<div class="relative">
				<img src={imagePreview} alt="Selected" class="max-h-48 rounded-lg shadow-md" />
				<button
					onclick={() => {
						selectedImage = null;
						imagePreview = null;
					}}
					class="leading-0 absolute right-2 top-2 m-0 aspect-square w-max cursor-pointer rounded bg-red-900 p-2 text-white"
				>
					&times;
				</button>
			</div>
		</div>
	{/if}

	<!-- Message input -->
	<div class="border-t bg-white p-4">
		<div class="mx-auto flex max-w-3xl items-center gap-2">
			<div class="relative flex-1">
				<!-- Input field with image upload icon inside -->
				<input
					type="text"
					name="message"
					bind:value={msg}
					onkeydown={handleKeyPress}
					placeholder="Type a message..."
					class="w-full rounded-full border px-4 py-2 pl-12 pr-12 focus:border-blue-500 focus:outline-none"
					disabled={isStreaming}
				/>
				<!-- Image upload icon -->
				<label for="image-upload" class="absolute left-3 top-1/2 -translate-y-1/2 cursor-pointer">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 24 24"
						fill="currentColor"
						class="h-6 w-6 text-gray-500 hover:text-gray-700"
					>
						<path
							fill-rule="evenodd"
							d="M4.5 3A1.5 1.5 0 003 4.5v15A1.5 1.5 0 004.5 21h15a1.5 1.5 0 001.5-1.5v-15A1.5 1.5 0 0019.5 3h-15zM4.5 4.5h15v15h-15v-15z"
							clip-rule="evenodd"
						/>
						<path
							d="M8.25 10.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM7.5 16.5l2.25-3 3 3.75 4.5-6 1.5 2.25v3h-12v-3z"
						/>
					</svg>
				</label>
				<input
					type="file"
					accept="image/*"
					onchange={handleImageChange}
					class="hidden"
					id="image-upload"
				/>
			</div>
			<button
				onclick={sendMessage}
				class="cursor-pointer rounded-full bg-blue-500 px-6 py-2 text-white transition-colors hover:bg-blue-600 disabled:cursor-not-allowed disabled:bg-gray-400"
				disabled={isStreaming || (!msg.trim() && !selectedImage)}
			>
				Send
			</button>
		</div>
	</div>
</div>
