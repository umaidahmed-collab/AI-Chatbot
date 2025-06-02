# Frontend - Wellows AI Chatbot Interface

## Overview

The frontend is a modern React application built with TypeScript that provides an intuitive user interface for the Wellows AI chatbot. It features real-time chat, document upload, user authentication, and responsive design.

## 🏗️ Architecture

```
frontend/
├── public/                # Static assets
│   ├── index.html        # Main HTML template
│   └── manifest.json     # PWA manifest
├── src/                  # Source code
│   ├── components/       # React components
│   │   ├── Auth/        # Authentication components
│   │   ├── Chat/        # Chat interface components
│   │   ├── Documents/   # Document management components
│   │   └── Layout/      # Layout and navigation components
│   ├── contexts/        # React contexts for state management
│   ├── services/        # API service layer
│   ├── types/           # TypeScript type definitions
│   ├── utils/           # Utility functions
│   ├── App.tsx          # Main application component
│   └── index.tsx        # Application entry point
├── package.json         # Dependencies and scripts
├── tsconfig.json        # TypeScript configuration
├── tailwind.config.js   # Tailwind CSS configuration
└── Dockerfile          # Container configuration
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Local Development
```bash
# Install dependencies
npm install

# Start development server
npm start

# Open browser to http://localhost:3000
```

### Using Dev Container
```bash
# Open in VS Code with Remote-Containers extension
# The environment will be automatically configured
runfrontend  # Alias to start the development server
```

## 🎨 Design System

### UI Framework
- **React 18**: Modern React with hooks and concurrent features
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Heroicons**: Beautiful SVG icons

### Component Structure
```
components/
├── Auth/
│   ├── Login.tsx         # Login form component
│   └── Register.tsx      # Registration form component
├── Chat/
│   ├── Chat.tsx          # Main chat interface
│   ├── ChatInput.tsx     # Message input component
│   ├── MessageList.tsx   # Message display component
│   └── SessionSidebar.tsx # Chat session management
├── Documents/
│   ├── Documents.tsx     # Document management page
│   ├── DocumentUpload.tsx # File upload component
│   └── DocumentList.tsx  # Document listing component
└── Layout/
    ├── Layout.tsx        # Main layout wrapper
    ├── Header.tsx        # Application header
    └── Sidebar.tsx       # Navigation sidebar
```

## 🔧 Configuration

### Environment Variables
```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000

# Feature Flags
REACT_APP_DEBUG=false
REACT_APP_ENABLE_ANALYTICS=false
```

### Build Configuration
- **Development**: Hot reload, source maps, debug tools
- **Production**: Minified, optimized, compressed assets

## 🧪 Testing

### Test Setup
- **Jest**: Testing framework
- **React Testing Library**: Component testing utilities
- **@testing-library/user-event**: User interaction simulation

### Run Tests
```bash
# Run all tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch

# Run specific test file
npm test -- Login.test.tsx
```

### Test Structure
```
src/
├── components/
│   └── __tests__/       # Component tests
├── services/
│   └── __tests__/       # Service tests
└── utils/
    └── __tests__/       # Utility tests
```

## 📦 Dependencies

### Core Dependencies
- **React**: UI library
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls
- **React Hot Toast**: Toast notifications

### Development Dependencies
- **TypeScript**: Type checking
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **Tailwind CSS**: Styling framework

## 🎯 Features

### Authentication
- User registration and login
- JWT token management
- Protected routes
- Automatic token refresh

### Chat Interface
- Real-time messaging
- Chat session management
- Message history
- Document-aware conversations
- Typing indicators
- Message timestamps

### Document Management
- Drag-and-drop file upload
- File type validation
- Upload progress tracking
- Document listing and management
- Processing status indicators

### Responsive Design
- Mobile-first approach
- Tablet and desktop optimization
- Touch-friendly interactions
- Accessible design patterns

## 🔄 State Management

### React Context
```typescript
// Authentication Context
interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  register: (userData: RegisterData) => Promise<boolean>;
  logout: () => void;
}

// Usage in components
const { user, login, logout } = useAuth();
```

### Local State
- Component-specific state with useState
- Form state management
- UI state (loading, errors, etc.)

## 🌐 API Integration

### Service Layer
```typescript
// API Service Structure
export const authService = {
  login: (username: string, password: string) => Promise<AuthResponse>,
  register: (userData: RegisterRequest) => Promise<User>,
  getCurrentUser: () => Promise<User>,
};

export const chatService = {
  sendMessage: (request: ChatRequest) => Promise<ChatResponse>,
  getSessions: () => Promise<ChatSession[]>,
  createSession: (title?: string) => Promise<ChatSession>,
};
```

### Error Handling
- Global error interceptors
- User-friendly error messages
- Retry mechanisms
- Offline support

## 🎨 Styling

### Tailwind CSS
```typescript
// Example component styling
<div className="bg-white rounded-lg shadow-sm border border-gray-200">
  <div className="p-6 border-b border-gray-200">
    <h2 className="text-lg font-semibold text-gray-900">Chat</h2>
  </div>
  <div className="p-4">
    {/* Content */}
  </div>
</div>
```

### Design Tokens
- **Colors**: Primary, secondary, success, warning, error
- **Typography**: Font sizes, weights, line heights
- **Spacing**: Consistent margin and padding scale
- **Shadows**: Elevation system
- **Borders**: Radius and width standards

## 📱 Responsive Design

### Breakpoints
```css
/* Tailwind CSS breakpoints */
sm: 640px   /* Small devices */
md: 768px   /* Medium devices */
lg: 1024px  /* Large devices */
xl: 1280px  /* Extra large devices */
2xl: 1536px /* 2X large devices */
```

### Mobile Optimization
- Touch-friendly button sizes
- Optimized navigation
- Responsive typography
- Mobile-specific interactions

## 🚀 Build & Deployment

### Development Build
```bash
npm start
# Starts development server with hot reload
```

### Production Build
```bash
npm run build
# Creates optimized production build in build/
```

### Docker Deployment
```bash
# Build image
docker build -t wellows-frontend .

# Run container
docker run -p 3000:80 wellows-frontend
```

## 🔍 Performance

### Optimization Strategies
- Code splitting with React.lazy()
- Image optimization
- Bundle size monitoring
- Lazy loading for components
- Memoization with React.memo()

### Performance Monitoring
- Core Web Vitals tracking
- Bundle analyzer
- Performance profiling
- Memory usage monitoring

## ♿ Accessibility

### WCAG Compliance
- Semantic HTML structure
- ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- Color contrast compliance

### Testing
```bash
# Accessibility testing
npm run test:a11y

# Lighthouse audit
npm run audit
```

## 🔧 Development Tools

### VS Code Extensions
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- TypeScript Importer
- Auto Rename Tag
- Prettier - Code formatter

### Browser Extensions
- React Developer Tools
- Redux DevTools (if using Redux)
- Lighthouse
- axe DevTools (accessibility)

## 🤝 Contributing

### Code Style
- Use TypeScript for all new code
- Follow React best practices
- Use functional components with hooks
- Implement proper error boundaries
- Write comprehensive tests

### Component Guidelines
```typescript
// Component template
interface ComponentProps {
  // Define props with TypeScript
}

const Component: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  // Component logic
  
  return (
    <div className="component-styles">
      {/* JSX content */}
    </div>
  );
};

export default Component;
```

## 🔧 Troubleshooting

### Common Issues

#### Build Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear build cache
npm start -- --reset-cache
```

#### TypeScript Errors
```bash
# Check TypeScript configuration
npx tsc --noEmit

# Update type definitions
npm update @types/*
```

#### Styling Issues
```bash
# Rebuild Tailwind CSS
npm run build:css

# Check Tailwind configuration
npx tailwindcss --help
```

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [React Router Documentation](https://reactrouter.com/)
