# Create GitHub repo (one-time)

Local commit ready: `ddf408e` on `main`.

1. Create empty repo: https://github.com/new  
   - Owner: `DeepSeekOracle`  
   - Name: `lygo-claw`  
   - Public, **no** README (already in tree)

2. Push:

```powershell
cd "I:\E Drive\lygo-claw"
python "I:\E Drive\lygo-protocol-stack\tools\push_with_git_credential.py"
# or after gh auth login:
gh repo create DeepSeekOracle/lygo-claw --public --source=. --push
```

3. Verify:

```powershell
git ls-remote https://github.com/DeepSeekOracle/lygo-claw.git refs/heads/main
```