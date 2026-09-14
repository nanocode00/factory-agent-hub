# AI Human 7th — Project2 요구사항

> 원문 웹페이지를 2026-09-14 기준으로 Markdown 형태로 보관한 문서입니다.
>
> - Source: https://checkpoint.habix.ai/aihuman-7th/project2
> - Linked guide PDF: https://checkpoint.habix.ai/downloads/2%EC%B0%A8_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EA%B0%80%EC%9D%B4%EB%93%9C_v3.pdf
> - Page title: 2차 프로젝트 — Checkpoint
> - 목적: 프로젝트 구현 중 요구사항 누락을 막기 위한 저장소 내 기준 문서

---

2nd Team Project · AI Human 7th

# 동작 가능한 버티컬 AGENT 만들기

내가 3개월 이상 직접 경험한 버티컬 도메인에서, 실제 사용자의 반복 업무를 해결하는 Agent를 만듭니다. 모델 호출이 아니라 도메인 규칙·도구·평가가 연결된 서비스로 완성합니다.

**주제 검증 기준** · 내가 그 도메인의 사용자·업무 흐름·예외 상황을 3개월 이상 경험했는가?

[가이드 PDF 열기 →](/downloads/2차_프로젝트_가이드_v3.pdf)우리 조 확인하기

Project path

시작부터 발표까지의 실행 경로

착수 → 결정 → 완성 → 발표

1. 09.14–17

   사전기획

   문제 후보 · 평가셋 후보
2. 09.18–23

   착수·설계

   주제 · 계약 · 평가 기준
3. 10.08

   구현 마감

   배포 · 측정 · 리포트
4. 10.12

   팀 발표

   증거와 함께 설명

First checkpoint

## 먼저, 내가 아는 도메인인지 확인합니다.

1. 01

   3개월 이상 경험

   내가 직접 겪은 사용자·업무 흐름·예외 상황을 구체적으로 설명합니다.
2. 02

   반복 업무

   Agent가 줄일 수 있는 반복 작업과 평가할 입력 30건의 기준을 잡습니다.

Definition of done

“돌아간다”는 주장이 아니라 증거입니다.

몇 건 중 몇 건이 출력 계약을 지켰는지, 실패하면 무엇으로 떨어지는지, 한 번 처리에 얼마가 드는지를 남이 확인할 수 있어야 합니다.

출력 계약실패 경로품질·비용

Delivery format

## 버티컬 Agent를 운영 가능한 서비스로 냅니다.

화면, Agent API, MCP 도구, 관측·평가를 한 실행 경로로 연결합니다. MCP는 제품 기능을 위한 도메인 도구이지, 공개 데모 API가 아닙니다.

일정·제출 보기

01

Vercel UI

사용자 입력·결과·실패 안내

증거 · Vercel URL

02

Cloud Run API

GET /health · POST /api/agent

증거 · Cloud Run URL

03

MCP 도구

도메인 데이터·행동을 /mcp로 제공

증거 · 호출 결과

04

Evidence loop

Docker · Langfuse · Prompt Management · Evals 재측정

증거 · README · EVAL\_REPORT

브라우저가 Cloud Run을 직접 호출한다면 CORS·인증·비밀값 노출 방식을 README에 설명하세요. `/api/agent`와 `/mcp`는 역할을 분리합니다.

Pre-planning

9/14~9/17 사전기획 과제부터 시작합니다.

문제 후보, 사용자 상황, 범위, 평가셋 후보를 개인별로 준비한 뒤 9/18에 조의 한 문장으로 합칩니다.

일별 계획 보기

[진행 현황 보기](/aihuman-7th/project2/board)[GitHub 조직 →](https://github.com/aihuman-7th)

이 페이지는 요약입니다. 필수 조건의 정확한 판정 기준, RAG 경계 사례 15종, 서비스 엔지니어링 5원칙, FAQ는 [2차 프로젝트 가이드 v3 PDF](/downloads/2차_프로젝트_가이드_v3.pdf)에서 확인하세요.
