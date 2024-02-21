#!/usr/bin/env bash
set -o errexit

cd backend/frontend
npm install
npm run build