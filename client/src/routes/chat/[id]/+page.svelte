<script module lang="ts">
	export interface PlotPoints {
		item_id: string;
		item_name: string;
		frequency: number;
		total_value: number;
	}

	export interface PlotPointsResponse {
		data_point: 'frequency' | 'total_value';
		data_points: {
			today: PlotPoints[];
			this_week: PlotPoints[];
			this_month: PlotPoints[];
		};
		time: 'today' | 'this_week' | 'this_month';
	}
</script>

<script lang="ts">
	import { enhance } from '$app/forms';
	import { afterNavigate } from '$app/navigation';
	import { PUBLIC_API_URL } from '$env/static/public';
	import PieChart from '$lib/components/PieChart.svelte';
	import type { ApexOptions } from 'apexcharts';
	import { marked } from 'marked';
	import sanitizeHtml from 'sanitize-html';
	import { tick } from 'svelte';
	import type { Message } from './+page.server.js';

	let { data } = $props();

	let msg = $state('');
	let messages: Message[] = $derived(data.messages);

	let textarea: HTMLTextAreaElement | null = $state(null);
	let isStreaming = $state(false);
	let currentStreamingMessage = $state('');
	let markdownStreamingMessage = $state('');
	let selectedImage: File | null = $state(null);
	let imagePreview: string | null = $state(null);
	let showThinking = $state(false);
	let thinkingMessage: HTMLDivElement | null = $state(null);

	const isJsonString = (str: string) => {
		try {
			JSON.parse(str);
		} catch (e) {
			return false;
		}
		return true;
	};

	const renderChart = async (msg: string, el: HTMLDivElement) => {
		const res: PlotPointsResponse = JSON.parse(msg);

		import('apexcharts').then((ApexCharts) => {
			const options: ApexOptions = {
				chart: {
					type: 'pie',
					foreColor: '#fefefe'
				},
				series: [
					{
						name: res.data_point,
						data: res.data_points[res.time].map((point) => point[res.data_point])
					}
				],
				dataLabels: {
					enabled: false
				},
				tooltip: {
					x: {
						show: true
					}
				}
			};
			new ApexCharts.default(el, options).render();
		});
	};

	const sanitizeOptions: sanitizeHtml.IOptions = {
		disallowedTagsMode: 'escape'
	};

	const resizeTextarea = () => {
		textarea!.style.height = '2.7rem'; // Reset height to auto
		textarea!.style.height = `${Math.min(textarea!.scrollHeight / 16, 9.5)}rem`; // Adjust height
	};

	let autoScrollEnabled = $state(true);
	let chatContainer: HTMLDivElement | null = $state(null);

	// Function to scroll to the bottom of the chat container
	const scrollToBottom = () => {
		if (chatContainer) {
			chatContainer.scrollTo({
				top: chatContainer.scrollHeight,
				behavior: 'smooth'
			});
		}
	};

	// Function to handle user scrolling
	const handleScroll = () => {
		if (chatContainer) {
			// Check if the user has scrolled up
			const isScrolledUp =
				chatContainer.scrollTop + chatContainer.clientHeight < chatContainer.scrollHeight - 50; // Add a small buffer (50px)
			autoScrollEnabled = !isScrolledUp;
		}
	};

	// Function to enable auto-scroll when the user presses the down arrow button
	const enableAutoScroll = () => {
		autoScrollEnabled = true;
		scrollToBottom();
	};
	afterNavigate(() => enableAutoScroll());

	const saveMessage = async (message: Message) => {
		await fetch(`${PUBLIC_API_URL}/chat/${data.chatId}/messages`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ ...message })
		});
	};

	const sendMessage = async () => {
		if (!msg.trim() && !selectedImage) return;
		if (isStreaming) return;

		setTimeout(() => {
			enableAutoScroll(); // Enable auto-scroll after sending a message
		}, 100);

		// Add user message to chat
		const userMessage: Message = {
			text: msg,
			is_sent: true,
			image: imagePreview ?? undefined
		};
		messages = [...messages, userMessage];
		msg = '';

		imagePreview = null;

		isStreaming = true;
		showThinking = true;
		currentStreamingMessage = '';

		await tick(); // Wait for DOM updates
		resizeTextarea(); // Reset textarea height

		try {
			let response;

			if (selectedImage) {
				const formData = new FormData();
				formData.append('image', selectedImage);
				formData.append('chat_id', String(data.chatId));

				response = await fetch(`${PUBLIC_API_URL}/ocr/generate`, {
					method: 'POST',
					body: formData
				});
			} else {
				response = await fetch(`${PUBLIC_API_URL}/ollama/generate`, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({ prompt: userMessage.text, merchant_id: data.user?.merchant_id })
				});
				saveMessage(userMessage);
			}

			if (response.headers.get('content-type') === 'application/json') {
				const res: PlotPointsResponse = await response.json();

				// Add the complete response to messages
				const finalMessage = { text: JSON.stringify(res), is_sent: false, image: undefined };
				messages = [...messages, finalMessage];
				await saveMessage(finalMessage);
			} else {
				const reader = response.body?.getReader();
				if (!reader) throw new Error('No reader available');

				while (true) {
					const { done, value } = await reader.read();
					if (done) break;

					// Convert the chunk to text and append it
					const chunk = new TextDecoder().decode(value);

					if (selectedImage) {
						currentStreamingMessage += chunk;
					} else {
						currentStreamingMessage = chunk;
					}

					markdownStreamingMessage = await marked.parse(currentStreamingMessage);
				}

				// Scroll to the bottom during streaming if auto-scroll is enabled
				if (autoScrollEnabled) {
					scrollToBottom();
				}

				// Add the complete response to messages
				const finalMessage = { text: markdownStreamingMessage, is_sent: false, image: undefined };
				messages = [...messages, finalMessage];
				await saveMessage(finalMessage);
			}

			currentStreamingMessage = '';
			markdownStreamingMessage = '';
		} catch (error) {
			console.error('Error:', error);
			messages = [
				...messages,
				{
					text: 'Sorry, there was an error processing your message.',
					is_sent: false,
					image: undefined
				}
			];
		} finally {
			isStreaming = false;
			showThinking = false;
			selectedImage = null;
		}
	};

	const handleKeyPress = (event: KeyboardEvent) => {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			sendMessage();
		}
	};

	const handleImageChange = (event: Event) => {
		const target = event.target as HTMLInputElement;
		selectedImage = target.files ? target.files[0] : null;
		msg = '';

		if (selectedImage) {
			const reader = new FileReader();
			reader.onload = () => {
				imagePreview = reader.result as string;
			};
			reader.readAsDataURL(selectedImage);
		} else {
			imagePreview = null;
		}
	};
</script>

<main class="bg-tertiary flex h-screen">
	<!-- Chat Section -->
	<section
		class="flex flex-1 items-center justify-center transition-all duration-300 peer-checked:w-full"
	>
		<!-- Chat box -->
		<div
			class="bg-primary relative flex h-[90%] w-[90%] max-w-4xl flex-col rounded-lg shadow-lg transition-all duration-300 peer-checked:w-[95%] peer-checked:max-w-none"
		>
			<div class="my-10 flex justify-center">
				<img src="/grab.svg" alt="Logo" class="h-20" />
			</div>

			<!-- Chat container -->
			<div class="flex-1 overflow-y-auto p-4" bind:this={chatContainer} onscroll={handleScroll}>
				<div class="mx-auto max-w-3xl space-y-4">
					{#each messages as message (message.id)}
						<div class="flex {message.is_sent ? 'justify-end' : 'justify-start'} items-start gap-2">
							{#if !message.is_sent}
								<!-- Profile picture for the chatbot-->
								<img src="/icons/bot.svg" alt="Other Party" class="h-8 w-8 rounded-lg" />
							{/if}
							<div
								class="prose bg-tertiary/[0.6] text-secondary {isJsonString(message.text)
									? 'w-[65%]'
									: 'w-fit'} rounded-lg p-3 shadow-sm"
							>
								{#if message.image}
									<img
										src={message.image}
										alt="Uploaded"
										class="max-h-40 max-w-full rounded-lg object-contain"
									/>
								{/if}

								{#if isJsonString(message.text)}
									<PieChart res={JSON.parse(message.text)} />
								{:else}
									{@html sanitizeHtml(message.text, sanitizeOptions)}
								{/if}
							</div>
							{#if message.is_sent}
								<!-- Profile picture for the user -->
								<img
									src={data.session?.user?.image ||
										`https://ui-avatars.com/api/?name=${data.user?.merchant.merchant_name}`}
									alt="You"
									class="h-8 w-8 rounded-lg"
								/>
							{/if}
						</div>
					{/each}

					{#if isStreaming}
						<div class="flex items-start justify-start gap-2">
							<!-- Profile picture for the chatbot -->
							<img src="/icons/bot.svg" alt="Chatbot" class="h-8 w-8 rounded-lg" />
							<div
								class="prose text-secondary bg-tertiary/[0.6] max-w-[70%] rounded-lg p-3 shadow-sm"
								bind:this={thinkingMessage}
							>
								{#if !markdownStreamingMessage}
									I am thinking<span class="ml-1 inline-flex gap-1">
										<span class="bg-secondary/[0.8] animate-dot-pulse h-2 w-2 rounded-full"></span>
										<span
											class="bg-secondary/[0.8] animate-dot-pulse h-2 w-2 rounded-full [animation-delay:200ms]"
										></span>
										<span
											class="bg-secondary/[0.8] animate-dot-pulse h-2 w-2 rounded-full [animation-delay:400ms]"
										></span>
									</span>
								{:else}
									{@html sanitizeHtml(markdownStreamingMessage, sanitizeOptions)}
								{/if}
							</div>
						</div>
					{/if}
				</div>
			</div>

			<!-- Down arrow button -->
			{#if !autoScrollEnabled}
				<button
					class="bg-highlight text-tertiary absolute bottom-5 right-5 cursor-pointer rounded-full p-2 shadow-lg"
					onclick={enableAutoScroll}
				>
					↓
				</button>
			{/if}

			<!-- Chat input box -->
			<div class="bg-primary rounded-lg p-4">
				<div class="mx-auto flex max-w-3xl items-center gap-2">
					<div class="relative flex-1">
						<!-- Textarea field -->
						<textarea
							name="message"
							bind:this={textarea}
							bind:value={msg}
							disabled={imagePreview !== null}
							onkeydown={handleKeyPress}
							placeholder="How can I help you?"
							class="bg-highlight text-tertiary placeholder-tertiary/[0.6] focus:border-secondary w-full resize-none rounded-lg border px-4 py-2 pl-12 pr-12 focus:outline-none"
							style="overflow-y: auto; max-height: 9.5rem; height: 2.7rem"
							oninput={resizeTextarea}
						></textarea>

						<!-- Image upload icon -->
						<label for="image-upload" class="absolute bottom-0 left-3 -translate-y-1/2">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 24 24"
								fill="currentColor"
								class=" hover:text-tertiary/[0.6] h-6 w-6 {msg !== ''
									? 'text-tertiary/[0.6] cursor-not-allowed'
									: 'text-tertiary cursor-pointer'}"
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
							disabled={msg !== ''}
							class="hidden"
							id="image-upload"
						/>

						<!-- Image preview -->
						{#if imagePreview}
							<div class="absolute left-0 top-0 translate-y-[-100%] p-2">
								<div class="relative aspect-square max-h-20 max-w-20">
									<img
										src={imagePreview}
										alt="Preview"
										class="h-full w-full rounded-lg border border-gray-300 object-cover shadow-sm"
									/>
									<!-- Close button -->
									<button
										onclick={() => {
											selectedImage = null;
											imagePreview = null;
										}}
										class="text-tertiary bg-secondary/[0.5] absolute right-1 top-1 flex h-5 w-5 cursor-pointer items-center justify-center rounded-full opacity-0 transition-opacity hover:opacity-100"
									>
										&times;
									</button>
								</div>
							</div>
						{/if}

						<!-- Send button -->
						<button
							onclick={sendMessage}
							class="text-tertiary hover:text-tertiary/[0.6] disabled:text-tertiary/[0.6] absolute bottom-1 right-3 flex -translate-y-1/2 cursor-pointer items-center justify-center transition-colors disabled:cursor-not-allowed"
							disabled={isStreaming || (!msg.trim() && !selectedImage)}
						>
							<!-- Send icon -->
							<svg
								width="20"
								height="19"
								viewBox="0 0 20 19"
								fill="none"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path
									d="M18.2638 10.9653C19.5052 10.3831 19.5053 8.61593 18.2631 8.03454L3.08912 0.921317C1.84313 0.337641 0.484155 1.47534 0.83816 2.80451L2.33582 8.42106L8.68872 8.42089C8.97162 8.4258 9.24127 8.54162 9.43958 8.74342C9.6379 8.94521 9.74902 9.21683 9.74902 9.49977C9.74901 9.78271 9.63787 10.0543 9.43954 10.2561C9.24121 10.4579 8.97156 10.5738 8.68866 10.5787L2.33576 10.5789L0.838558 16.1963C0.483717 17.5247 1.84339 18.6616 3.08865 18.0786L18.2638 10.9653Z"
									fill="currentColor"
								/>
							</svg>
						</button>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- Aside Section -->
	<label
		for="toggle-aside"
		class="bg-secondary text-tertiary absolute right-4 top-4 cursor-pointer rounded px-2 py-1"
	>
		☰
	</label>
	<!-- Hidden checkbox for toggling the aside -->
	<input type="checkbox" id="toggle-aside" class="peer hidden" />
	<aside class="bg-primary h-screen w-1/4 overflow-y-auto p-4 peer-checked:hidden">
		<!-- Add content for the aside section here -->
		<h2 class="text-lg font-bold text-white">Chats</h2>
		<p class="text-white">All your chats in one place</p>

		<form action="?/createChat" method="POST" use:enhance>
			<!-- + New Chat Button -->
			<button
				class="bg-highlight text-tertiary text-mdsemi mt-4 w-full cursor-pointer rounded-lg px-4 py-2"
			>
				&plus; &nbsp; New Chat
			</button>
		</form>

		<!-- Dummy Chat List -->
		<ul class="mt-4 space-y-2">
			{#each data.chats as chat}
				<li
					class="{chat.id === data.chatId
						? 'bg-secondary/[0.8]'
						: ''} bg-secondary/[0.5] hover:bg-secondary/[0.8] cursor-pointer rounded-lg p-3 text-white"
				>
					<a href="/chat/{chat.id}" class="flex h-full w-full gap-2">
						<img src="/icons/message.svg" alt="message icon" />
						<span class="text-md">{chat.name}</span>
					</a>
				</li>
			{/each}
		</ul>
	</aside>
</main>

<style lang="postcss">
	@keyframes dot-pulse {
		0%,
		40%,
		100% {
			opacity: 0.3;
			transform: scale(0.85);
		}
		20% {
			opacity: 1;
			transform: scale(1);
		}
	}
</style>
