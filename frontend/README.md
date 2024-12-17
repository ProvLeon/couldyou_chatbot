# CouldYou? Cup Chat Assistant Frontend

A modern chat interface built with Next.js for the CouldYou? Cup menstrual health chatbot. This frontend provides an intuitive way to interact with the AI assistant to get answers about menstrual health and period poverty.

## Features

- 💬 Real-time chat interface with AI responses
- 🎨 Clean and responsive design using Tailwind CSS
- ✨ Smooth animations using Framer Motion
- 📝 Markdown support for formatted messages
- 🔄 Auto-growing input field
- 📱 Mobile-friendly layout
- 🌐 Internationalization support
- ⌨️ Keyboard shortcuts
- 📋 Copy message functionality
- 🎭 User/Bot avatars and timestamps

## Tech Stack

- [Next.js 13+](https://nextjs.org/) - React framework
- [TypeScript](https://www.typescriptlang.org/) - Type safety
- [Tailwind CSS](https://tailwindcss.com/) - Styling
- [Framer Motion](https://www.framer.com/motion/) - Animations
- [React Markdown](https://github.com/remarkjs/react-markdown) - Message formatting
- [React Icons](https://react-icons.github.io/react-icons/) - UI icons
- [date-fns](https://date-fns.org/) - Date formatting

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/couldyou-chatbot.git
cd couldyou-chatbot/frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
# or
pnpm install
```

3. Set up environment variables:
Create a `.env.local` file with:
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
```

4. Run the development server:
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) to see the application.

## Project Structure

```
frontend/
├── app/                   # Next.js app directory
├── components/           # React components
│   ├── ChatInput.tsx    # Message input component
│   ├── ChatMessage.tsx  # Individual message component
│   ├── ChatWindow.tsx   # Main chat interface
│   └── ...
├── context/             # React context
│   └── ChatContext.tsx  # Chat state management
├── public/             # Static assets
├── styles/            # Global styles
└── utils/             # Utility functions
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build production bundle
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Vercel](https://vercel.com) for Next.js
- [Tailwind Labs](https://tailwindcss.com) for Tailwind CSS
- All contributors and maintainers

## Support

For support, email support@couldyoucup.org or join our Slack channel.
