```tsx {1-4|6-10|12-15|17}{maxHeight:'340px'}
// src/Greeting.tsx

interface GreetingProps {
  name: string;
  role?: string;  // ? = 선택적 prop (없어도 오류 없음)
}

function Greeting({ name, role }: GreetingProps) {
  return (
    <div>
      <h1>안녕하세요, {name}님!</h1>
      {role && <p>역할: {role}</p>}
    </div>
  );
}

export default Greeting;
```