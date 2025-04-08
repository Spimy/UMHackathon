<script lang="ts">
	let msg = $state('');
	let messages = $state([
		{ text: 'Hey there! 👋', isSent: false },
		{ text: 'Hi! How are you?', isSent: true },
		{ text: "I'm doing great, thanks for asking!", isSent: false }
	]);
	let isStreaming = $state(false);
	let currentStreamingMessage = $state('');

	async function sendMessage() {
		if (!msg.trim() || isStreaming) return;

		// Add user message to chat
		const userMessage = msg;
		msg = '';
		messages = [...messages, { text: userMessage, isSent: true }];

		isStreaming = true;
		currentStreamingMessage = '';

		try {
			const response = await fetch('http://localhost:8000/ollama/generate', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ prompt: userMessage })
			});

			const reader = response.body?.getReader();
			if (!reader) throw new Error('No reader available');

			while (true) {
				const { done, value } = await reader.read();
				if (done) break;

				// Convert the chunk to text and append it
				const chunk = new TextDecoder().decode(value);
				currentStreamingMessage += chunk;
			}

			// Add the complete response to messages
			messages = [...messages, { text: currentStreamingMessage, isSent: false }];
			currentStreamingMessage = '';
		} catch (error) {
			console.error('Error:', error);
			messages = [
				...messages,
				{ text: 'Sorry, there was an error processing your message.', isSent: false }
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

	<!-- Message input -->
	<div class="border-t bg-white p-4">
		<div class="mx-auto flex max-w-3xl gap-2">
			<input
				type="text"
				name="message"
				bind:value={msg}
				onkeydown={handleKeyPress}
				placeholder="Type a message..."
				class="flex-1 rounded-full border px-4 py-2 focus:border-blue-500 focus:outline-none"
				disabled={isStreaming}
			/>
			<button
				onclick={sendMessage}
				class="rounded-full bg-blue-500 px-6 py-2 text-white transition-colors hover:bg-blue-600 disabled:cursor-not-allowed disabled:bg-gray-400"
				disabled={isStreaming || !msg.trim()}
			>
				Send
			</button>
		</div>
	</div>
</div>
